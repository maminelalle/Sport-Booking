"""
Models pour l'authentification et gestion des utilisateurs.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Role(models.Model):
    """Rôles disponibles dans le système."""
    
    ROLE_CHOICES = (
        ('CLIENT', 'Client'),
        ('MANAGER', 'Gestionnaire'),
        ('ADMIN', 'Administrateur'),
    )
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Rôle'
        verbose_name_plural = 'Rôles'
    
    def __str__(self):
        return self.get_name_display()


class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé."""
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Le numéro de téléphone doit contenir 9 à 15 chiffres'
            )
        ],
        blank=True
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # RGPD - suppression de compte
    gdpr_consent = models.BooleanField(default=False)
    
    # Override ManyToMany relationships with related_name to avoid clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur."""
        return f'{self.first_name} {self.last_name}'.strip()
