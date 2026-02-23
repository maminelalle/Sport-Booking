"""
Tests pour les modèles de paiement.
"""

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.auth_app.models import Role, CustomUser
from apps.sites.models import Site
from apps.courts.models import Court
from apps.reservations.models import Reservation
from apps.payments.models import Payment


class PaymentTestCase(TestCase):
    def setUp(self):
        # Créer les rôles
        manager_role = Role.objects.create(name='MANAGER')
        client_role = Role.objects.create(name='CLIENT')
        
        # Créer les utilisateurs
        self.manager = CustomUser.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password',
            role=manager_role
        )
        
        self.client = CustomUser.objects.create_user(
            username='client',
            email='client@example.com',
            password='password',
            role=client_role
        )
        
        # Créer un site
        self.site = Site.objects.create(
            name='Centre Sportif Paris',
            address='123 Rue de Paris',
            city='Paris',
            postal_code='75001',
            latitude=48.8566,
            longitude=2.3522,
            manager=self.manager
        )
        
        # Créer un terrain
        self.court = Court.objects.create(
            name='Terrain 1',
            sport_type='TENNIS',
            site=self.site,
            price_per_hour=25.00
        )
        
        # Créer une réservation
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        self.reservation = Reservation.objects.create(
            user=self.client,
            court=self.court,
            start_datetime=start,
            end_datetime=end,
            price_per_hour=25.00,
            total_amount=25.00,
            status='PENDING'
        )
    
    def test_payment_creation(self):
        """Tester la création d'un paiement."""
        payment = Payment.objects.create(
            reservation=self.reservation,
            amount=25.00,
            currency='EUR',
            method='STRIPE',
            status='PENDING'
        )
        
        self.assertEqual(payment.amount, 25.00)
        self.assertEqual(payment.status, 'PENDING')
        self.assertEqual(payment.reservation.id, self.reservation.id)
    
    def test_mark_payment_as_paid(self):
        """Tester le marquage d'un paiement comme payé."""
        payment = Payment.objects.create(
            reservation=self.reservation,
            amount=25.00,
            currency='EUR',
            method='STRIPE',
            status='PENDING'
        )
        
        payment.mark_as_paid()
        
        self.assertEqual(payment.status, 'SUCCESS')
        self.assertIsNotNone(payment.paid_at)
        
        # La réservation doit être confirmée
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'CONFIRMED')
