"""
Sérialiseurs pour la gestion des paiements.
"""

from rest_framework import serializers
from apps.payments.models import Payment, Invoice


class PaymentSerializer(serializers.ModelSerializer):
    reservation_details = serializers.SerializerMethodField()
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    method_name = serializers.CharField(source='get_method_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'reservation', 'reservation_details', 'amount', 'currency',
            'method', 'method_name', 'status', 'status_name',
            'transaction_reference', 'created_at', 'paid_at'
        ]
        read_only_fields = [
            'id', 'amount', 'currency', 'method', 'status',
            'transaction_reference', 'created_at', 'paid_at'
        ]
    
    def get_reservation_details(self, obj):
        from apps.reservations.serializers import ReservationListSerializer
        return ReservationListSerializer(obj.reservation).data


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['reservation', 'method']
    
    def create(self, validated_data):
        reservation = validated_data['reservation']
        validated_data['amount'] = reservation.total_amount
        validated_data['currency'] = 'EUR'
        return super().create(validated_data)


class StripePaymentIntentSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    
    def validate_reservation_id(self, value):
        from apps.reservations.models import Reservation
        try:
            reservation = Reservation.objects.get(id=value)
            if reservation.status != 'PENDING':
                raise serializers.ValidationError("Cette réservation a déjà été payée.")
        except Reservation.DoesNotExist:
            raise serializers.ValidationError("Réservation non trouvée.")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'pdf_file', 'created_at']
        read_only_fields = ['id', 'invoice_number', 'created_at']
