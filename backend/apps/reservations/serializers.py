"""
Sérialiseurs pour la gestion des réservations.
"""

from rest_framework import serializers
from apps.reservations.models import Reservation
from apps.courts.serializers import CourtListSerializer


class ReservationSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    court_details = CourtListSerializer(source='court', read_only=True)
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    can_cancel = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'user_email', 'court', 'court_details',
            'start_datetime', 'end_datetime', 'price_per_hour',
            'total_amount', 'status', 'status_name', 'notes', 'can_cancel',
            'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'price_per_hour', 'total_amount', 'created_at'
        ]
    
    def get_can_cancel(self, obj):
        return obj.can_be_cancelled()


class ReservationCreateSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True, required=True)
    start_datetime = serializers.DateTimeField(required=True)
    end_datetime = serializers.DateTimeField(required=True)
    
    class Meta:
        model = Reservation
        fields = [
            'court', 'start_datetime', 'end_datetime', 'notes', 'user_email'
        ]
    
    def validate(self, data):
        """Valider les dates et l'utilisateur."""
        if data['start_datetime'] >= data['end_datetime']:
            raise serializers.ValidationError("La date de début doit être avant la date de fin.")
        return data
    
    def create(self, validated_data):
        from apps.auth_app.models import CustomUser
        from decimal import Decimal, ROUND_HALF_UP
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            user_email = validated_data.pop('user_email')
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'user_email': 'Utilisateur non trouvé avec cet email.'})
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'utilisateur: {e}")
            raise
        
        try:
            # Get court and calculate price
            court = validated_data.get('court')
            start_datetime = validated_data.get('start_datetime')
            end_datetime = validated_data.get('end_datetime')
            
            # Calculate duration in hours
            duration = (end_datetime - start_datetime).total_seconds() / 3600
            
            # Get price per hour from court and ensure it's Decimal
            price_per_hour = Decimal(str(court.price_per_hour))
            total_amount = Decimal(str(duration)) * price_per_hour
            
            # Round to 2 decimal places
            total_amount = total_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            validated_data['user'] = user
            validated_data['price_per_hour'] = price_per_hour
            validated_data['total_amount'] = total_amount
            
            return super().create(validated_data)
        except serializers.ValidationError:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la création de la réservation: {str(e)}", exc_info=True)
            raise serializers.ValidationError(f"Erreur lors de la création: {str(e)}")


class ReservationListSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source='court.name', read_only=True)
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'court_name', 'start_datetime', 'end_datetime',
            'total_amount', 'status', 'status_name'
        ]


class ReservationCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)
