"""
Models pour la gestion des terrains et équipements.
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.sites.models import Site


class Equipment(models.Model):
    """Modèle pour les équipements disponibles."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Nom d'icône, ex: "wifi"
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Équipement'
        verbose_name_plural = 'Équipements'
    
    def __str__(self):
        return self.name


class Court(models.Model):
    """Modèle représentant un terrain de sport."""
    
    SPORT_TYPES = (
        ('TENNIS', 'Tennis'),
        ('FOOTBALL', 'Football'),
        ('BASKETBALL', 'Basketball'),
        ('BADMINTON', 'Badminton'),
        ('VOLLEYBALL', 'Volleyball'),
        ('SQUASH', 'Squash'),
        ('PING_PONG', 'Ping-pong'),
        ('PADEL', 'Padel'),
        ('HAND', 'Handball'),
        ('OTHER', 'Autre'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sport_type = models.CharField(max_length=50, choices=SPORT_TYPES)
    
    # Site d'appartenance
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='courts')
    
    # Tarification
    price_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    
    # Équipements
    equipments = models.ManyToManyField(Equipment, blank=True, related_name='courts')
    
    # Statut
    is_active = models.BooleanField(default=True)
    
    # Capacité
    capacity = models.PositiveIntegerField(default=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['site', 'name']
        verbose_name = 'Terrain'
        verbose_name_plural = 'Terrains'
        indexes = [
            models.Index(fields=['site']),
            models.Index(fields=['sport_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_sport_type_display()})"


class CourtImage(models.Model):
    """Images des terrains."""
    
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='courts/images/')
    title = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
        verbose_name = 'Image de terrain'
        verbose_name_plural = 'Images de terrains'
    
    def __str__(self):
        return f"Image de {self.court.name}"
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il y a une image principale
        if self.is_primary:
            CourtImage.objects.filter(court=self.court, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class BlockedPeriod(models.Model):
    """Périodes bloquées manuellement par le gestionnaire."""
    
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='blocked_periods')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_datetime']
        verbose_name = 'Période bloquée'
        verbose_name_plural = 'Périodes bloquées'
        indexes = [
            models.Index(fields=['court', 'start_datetime']),
        ]
    
    def __str__(self):
        return f"Bloqué: {self.court.name} ({self.start_datetime} - {self.end_datetime})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")
