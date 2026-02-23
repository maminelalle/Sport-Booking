"""
Models pour la gestion des sites (complexes sportifs).
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.auth_app.models import CustomUser


class Site(models.Model):
    """Modèle représentant un complexe sportif."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    
    # Coordonnées GPS
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    
    # Manager du site
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='managed_sites',
        limit_choices_to={'role__name': 'MANAGER'}
    )
    
    # Statut
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['manager']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class OpeningHours(models.Model):
    """Horaires d'ouverture du site selon les jours de la semaine."""
    
    DAYS_OF_WEEK = (
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    )
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='opening_hours')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    open_time = models.TimeField()
    close_time = models.TimeField()
    
    class Meta:
        unique_together = ('site', 'day_of_week')
        ordering = ['day_of_week']
    
    def __str__(self):
        return f"{self.site.name} - {self.get_day_of_week_display()}"


class SiteImage(models.Model):
    """Images des sites sportifs."""
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='sites/images/')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
        verbose_name = 'Image de site'
        verbose_name_plural = 'Images de sites'
    
    def __str__(self):
        return f"Image de {self.site.name}"
    
    def save(self, *args, **kwargs):
        # Si c'est marqué comme image primaire, retirer le flag des autres
        if self.is_primary:
            SiteImage.objects.filter(site=self.site).update(is_primary=False)
        super().save(*args, **kwargs)
        verbose_name = 'Horaires d\'ouverture'
        verbose_name_plural = 'Horaires d\'ouverture'
    
    def __str__(self):
        return f"{self.get_day_of_week_display()} ({self.site.name}): {self.open_time} - {self.close_time}"
