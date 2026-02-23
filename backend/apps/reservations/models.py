"""
Models pour la gestion des réservations.
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.auth_app.models import CustomUser
from apps.courts.models import Court


class Reservation(models.Model):
    """Modèle représentant une réservation."""
    
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('CANCELLED', 'Annulée'),
        ('COMPLETED', 'Terminée'),
    )
    
    # Informations de base
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reservations',
        limit_choices_to={'role__name': 'CLIENT'}
    )
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='reservations')
    
    # Plage horaire
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    
    # Tarification (figée au moment de la réservation)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-start_datetime']
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['court']),
            models.Index(fields=['start_datetime']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Réservation {self.id} - {self.court.name} ({self.start_datetime})"
    
    def can_be_cancelled(self):
        """Vérifie si la réservation peut être annulée (24h avant)."""
        from datetime import timedelta
        now = timezone.now()
        return (self.start_datetime - now) >= timedelta(hours=24)
    
    def cancel(self):
        """Annule la réservation."""
        if self.status == 'CANCELLED':
            return False
        self.status = 'CANCELLED'
        self.cancelled_at = timezone.now()
        self.save()
        return True
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")
        
        # Vérifier chevauchement avec d'autres réservations confirmées
        overlapping = Reservation.objects.filter(
            court=self.court,
            status__in=['CONFIRMED', 'PENDING'],
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime
        ).exclude(pk=self.pk)
        
        if overlapping.exists():
            raise ValidationError("Ce créneau ne est pas disponible (chevauchement avec une autre réservation).")
    
    def save(self, *args, **kwargs):
        if not self.price_per_hour:
            self.price_per_hour = self.court.price_per_hour
        if not self.total_amount:
            duration_hours = (self.end_datetime - self.start_datetime).total_seconds() / 3600
            self.total_amount = float(self.price_per_hour) * duration_hours
        self.full_clean()
        super().save(*args, **kwargs)
