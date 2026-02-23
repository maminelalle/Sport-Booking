"""
Vues pour la gestion des réservations.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta

from apps.reservations.models import Reservation
from apps.reservations.serializers import (
    ReservationSerializer,
    ReservationCreateSerializer,
    ReservationListSerializer,
    ReservationCancelSerializer
)
from apps.core.permissions import IsClient, IsManager, IsAdmin, IsOwnReservation
from apps.auth_app.models import CustomUser


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des réservations."""
    
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'court__site']
    search_fields = ['court__name', 'user__email']
    ordering_fields = ['start_datetime', 'created_at']
    ordering = ['-start_datetime']
    
    def get_queryset(self):
        user = self.request.user
        user_email = self.request.query_params.get('user_email', None)
        
        # If user_email is provided as query param, filter by that
        if user_email:
            try:
                user_obj = CustomUser.objects.get(email=user_email)
                return Reservation.objects.filter(user=user_obj)
            except CustomUser.DoesNotExist:
                return Reservation.objects.none()
        
        # Otherwise use authenticated user
        if user and user.is_authenticated:
            if hasattr(user, 'role') and user.role:
                if user.role.name == 'CLIENT':
                    return Reservation.objects.filter(user=user)
                elif user.role.name == 'MANAGER':
                    return Reservation.objects.filter(court__site__manager=user)
        return Reservation.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        elif self.action == 'list':
            return ReservationListSerializer
        return ReservationSerializer
    
    def perform_create(self, serializer):
        """Créer une réservation."""
        reservation = serializer.save()
        return reservation
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsClient])
    def my_reservations(self, request):
        """Récupérer les réservations de l'utilisateur connecté."""
        reservations = Reservation.objects.filter(
            user=request.user
        ).order_by('-start_datetime')
        
        page = self.paginate_queryset(reservations)
        if page is not None:
            serializer = ReservationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnReservation])
    def cancel(self, request, pk=None):
        """Annuler une réservation."""
        reservation = self.get_object()
        
        if not reservation.can_be_cancelled():
            return Response(
                {'error': 'Cette réservation ne peut pas être annulée (< 24h avant la date).'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if reservation.cancel():
            return Response({
                'message': 'Réservation annulée avec succès',
                'reservation': ReservationSerializer(reservation).data
            })
        
        return Response(
            {'error': 'Impossible d\'annuler cette réservation'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def test_auth(self, request):
        """Test endpoint pour vérifier l'authentification."""
        return Response({
            'authenticated': request.user.is_authenticated,
            'user_id': request.user.id if request.user.is_authenticated else None,
            'user_email': request.user.email if request.user.is_authenticated else None,
            'user_role': request.user.role.name if (request.user.is_authenticated and hasattr(request.user, 'role')) else None,
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def check_availability(self, request):
        """Vérifier la disponibilité d'une plage horaire."""
        court_id = request.data.get('court_id')
        start = request.data.get('start')
        end = request.data.get('end')
        
        if not all([court_id, start, end]):
            return Response(
                {'error': 'court_id, start et end requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils.dateparse import parse_datetime
        from apps.courts.models import Court
        
        try:
            court = Court.objects.get(id=court_id)
        except Court.DoesNotExist:
            return Response(
                {'error': 'Terrain non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)
        
        # Vérifier les réservations qui se chevauchent
        overlapping = Reservation.objects.filter(
            court=court,
            status__in=['CONFIRMED', 'PENDING'],
            start_datetime__lt=end_dt,
            end_datetime__gt=start_dt
        ).exists()
        
        # Vérifier les périodes bloquées
        blocked = court.blocked_periods.filter(
            start_datetime__lt=end_dt,
            end_datetime__gt=start_dt
        ).exists()
        
        is_available = not (overlapping or blocked)
        
        return Response({
            'court_id': court.id,
            'is_available': is_available,
            'start': start,
            'end': end,
            'price_per_hour': float(court.price_per_hour)
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsManager | IsAdmin])
    def site_stats(self, request):
        """Récupérer les statistiques de réservations pour le site du manager."""
        user = request.user
        site_id = request.query_params.get('site_id')
        
        if user.role.name == 'MANAGER':
            reservations = Reservation.objects.filter(
                court__site__manager=user,
                court__site__id=site_id
            )
        else:
            reservations = Reservation.objects.filter(court__site__id=site_id)
        
        total_reservations = reservations.count()
        confirmed_reservations = reservations.filter(status='CONFIRMED').count()
        total_revenue = sum(r.total_amount for r in reservations.filter(status='CONFIRMED'))
        
        return Response({
            'total_reservations': total_reservations,
            'confirmed_reservations': confirmed_reservations,
            'total_revenue': float(total_revenue),
            'occupancy_rate': (confirmed_reservations / total_reservations * 100) if total_reservations > 0 else 0
        })
