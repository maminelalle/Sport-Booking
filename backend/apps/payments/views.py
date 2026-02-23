"""
Vues pour la gestion des paiements.
"""

import stripe
import json
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from apps.payments.models import Payment, Invoice
from apps.payments.serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    StripePaymentIntentSerializer,
    InvoiceSerializer
)
from apps.reservations.models import Reservation
from apps.core.permissions import IsClient

logger = logging.getLogger(__name__)

# Configurer Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des paiements."""
    
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'method']
    
    def get_queryset(self):
        from apps.auth_app.models import CustomUser
        
        user = self.request.user
        user_email = self.request.query_params.get('user_email', None)
        
        # If user_email is provided, use that
        if user_email:
            try:
                user_obj = CustomUser.objects.get(email=user_email)
                return Payment.objects.filter(reservation__user=user_obj)
            except CustomUser.DoesNotExist:
                return Payment.objects.none()
        
        # Otherwise use authenticated user
        if user and user.is_authenticated and hasattr(user, 'role') and user.role:
            if user.role.name == 'CLIENT':
                return Payment.objects.filter(reservation__user=user)
            elif user.role.name == 'MANAGER':
                return Payment.objects.filter(reservation__court__site__manager=user)
        return Payment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_payment_intent(self, request):
        """Créer un Payment Intent Stripe."""
        serializer = StripePaymentIntentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                reservation_id = serializer.validated_data['reservation_id']
                reservation = Reservation.objects.get(id=reservation_id)
                
                # Vérifier que l'utilisateur est propriétaire de la réservation
                if reservation.user != request.user:
                    return Response(
                        {'error': 'Vous ne pouvez pas payer pour cette réservation'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Créer ou récupérer le paiement
                payment, created = Payment.objects.get_or_create(
                    reservation=reservation,
                    defaults={
                        'amount': reservation.total_amount,
                        'currency': 'EUR',
                        'method': 'STRIPE'
                    }
                )
                
                if payment.status != 'PENDING':
                    return Response(
                        {'error': 'Ce paiement a déjà été traité'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Créer le Payment Intent
                intent = stripe.PaymentIntent.create(
                    amount=int(float(payment.amount) * 100),  # Convertir en centimes
                    currency=payment.currency.lower(),
                    description=f'Réservation {reservation.id} - {reservation.court.name}',
                    metadata={
                        'payment_id': payment.id,
                        'reservation_id': reservation.id
                    }
                )
                
                ## Sauvegarder l'ID du Payment Intent
                payment.stripe_payment_intent_id = intent.id
                payment.save()
                
                return Response({
                    'payment_intent_id': intent.id,
                    'client_secret': intent.client_secret,
                    'amount': float(payment.amount),
                    'currency': payment.currency
                }, status=status.HTTP_201_CREATED)
            
            except Reservation.DoesNotExist:
                return Response(
                    {'error': 'Réservation non trouvée'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except stripe.error.StripeError as e:
                logger.error(f"Stripe error: {str(e)}")
                return Response(
                    {'error': f'Erreur Stripe: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm_payment(self, request):
        """Confirmer le paiement après validation Stripe."""
        payment_intent_id = request.data.get('payment_intent_id')
        
        if not payment_intent_id:
            return Response(
                {'error': 'payment_intent_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Récupérer le Payment Intent Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status != 'succeeded':
                return Response(
                    {'error': 'Le paiement n\'a pas été approuvé'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Récupérer le paiement
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
            
            # Marquer le paiement comme réussi
            payment.status = 'SUCCESS'
            payment.stripe_charge_id = intent.latest_charge
            payment.transaction_reference = intent.id
            payment.paid_at = timezone.now()
            payment.save()
            
            # Confirmer la réservation
            reservation = payment.reservation
            reservation.status = 'CONFIRMED'
            reservation.save()
            
            # Créer une facture
            Invoice.objects.get_or_create(payment=payment)
            
            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_200_OK
            )
        
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Paiement non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return Response(
                {'error': f'Erreur Stripe: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def refund(self, request, pk=None):
        """Rembourser un paiement."""
        payment = self.get_object()
        
        # Vérifier les permissions
        if payment.reservation.user != request.user and request.user.role.name != 'ADMIN':
            return Response(
                {'error': 'Vous ne pouvez pas rembourser ce paiement'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if payment.status != 'SUCCESS':
            return Response(
                {'error': 'Seuls les paiements approuvés peuvent être remboursés'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Rembourser via Stripe
            refund = stripe.Refund.create(
                payment_intent=payment.stripe_payment_intent_id
            )
            
            # Mettre à jour le paiement
            payment.status = 'REFUNDED'
            payment.save()
            
            # Annuler la réservation
            payment.reservation.cancel()
            
            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_200_OK
            )
        
        except stripe.error.StripeError as e:
            logger.error(f"Stripe refund error: {str(e)}")
            return Response(
                {'error': f'Erreur lors du remboursement: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les factures."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        user = self.request.user
        if user.role.name == 'CLIENT':
            return Invoice.objects.filter(payment__reservation__user=user)
        elif user.role.name == 'MANAGER':
            return Invoice.objects.filter(payment__reservation__court__site__manager=user)
        return Invoice.objects.all()
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Télécharger une facture en PDF."""
        invoice = self.get_object()
        
        if not invoice.pdf_file:
            return Response(
                {'error': 'Facture PDF non disponible'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'url': invoice.pdf_file.url,
            'invoice_number': invoice.invoice_number
        })


@csrf_exempt
def stripe_webhook(request):
    """Webhook pour traiter les événements Stripe."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Traiter les événements pertinents
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_success(payment_intent)
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_failed(payment_intent)
    
    return JsonResponse({'status': 'success'})


def handle_payment_success(payment_intent):
    """Gérer le succès d'un paiement."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent.id)
        payment.mark_as_paid()
        logger.info(f"Payment {payment.id} marked as successful")
    except Payment.DoesNotExist:
        logger.warning(f"Payment Intent {payment_intent.id} not found in database")


def handle_payment_failed(payment_intent):
    """Gérer l'échec d'un paiement."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent.id)
        payment.status = 'FAILED'
        payment.save()
        logger.info(f"Payment {payment.id} marked as failed")
    except Payment.DoesNotExist:
        logger.warning(f"Payment Intent {payment_intent.id} not found in database")
