"""
Models pour la gestion des paiements.
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.reservations.models import Reservation


class Payment(models.Model):
    """Modèle représentant un paiement."""
    
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('SUCCESS', 'Réussi'),
        ('FAILED', 'Échoué'),
        ('REFUNDED', 'Remboursé'),
    )
    
    METHOD_CHOICES = (
        ('STRIPE', 'Stripe'),
        ('PAYPAL', 'PayPal'),
        ('CARD', 'Carte bancaire'),
        ('TRANSFER', 'Virement'),
    )
    
    CURRENCY_CHOICES = (
        ('EUR', '€ Euro'),
        ('USD', '$ Dollar US'),
        ('GBP', '£ Livre sterling'),
    )
    
    # Relation avec la réservation
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    
    # Montant et devise
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    
    # Méthode de paiement
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Références Stripe
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, unique=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True)
    
    # Références PayPal
    paypal_transaction_id = models.CharField(max_length=255, blank=True)
    
    # Générique - référence de transaction
    transaction_reference = models.CharField(max_length=255, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        indexes = [
            models.Index(fields=['reservation']),
            models.Index(fields=['status']),
            models.Index(fields=['stripe_payment_intent_id']),
        ]
    
    def __str__(self):
        return f"Paiement {self.id} - Réservation {self.reservation.id} ({self.status})"
    
    def mark_as_paid(self):
        """Marque le paiement comme réussi."""
        if self.status == 'SUCCESS':
            return False
        self.status = 'SUCCESS'
        from django.utils import timezone
        self.paid_at = timezone.now()
        # Valider la réservation
        reservation = self.reservation
        reservation.status = 'CONFIRMED'
        reservation.save()
        self.save()
        return True
    
    def refund(self):
        """Marque le paiement comme remboursé."""
        if self.status in ['REFUNDED', 'PENDING']:
            return False
        self.status = 'REFUNDED'
        self.save()
        # Annuler la réservation
        reservation = self.reservation
        reservation.cancel()
        return True


class Invoice(models.Model):
    """Modèle représentant une facture."""
    
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='invoices/', blank=True)
    
    # Détails
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Facture {self.invoice_number}"
    
    def generate_invoice_number(self):
        """Génère un numéro de facture unique."""
        from datetime import datetime
        year = datetime.now().year
        # Compter les factures du mois
        month = datetime.now().month
        count = Invoice.objects.filter(
            created_at__year=year,
            created_at__month=month
        ).count() + 1
        return f"INV-{year}-{month:02d}-{count:05d}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)
