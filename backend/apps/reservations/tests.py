"""
Tests pour les modèles de réservation.
"""

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.auth_app.models import Role, CustomUser
from apps.sites.models import Site
from apps.courts.models import Court
from apps.reservations.models import Reservation


class ReservationTestCase(TestCase):
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
    
    def test_reservation_creation(self):
        """Tester la création d'une réservation."""
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        reservation = Reservation.objects.create(
            user=self.client,
            court=self.court,
            start_datetime=start,
            end_datetime=end,
            price_per_hour=25.00,
            total_amount=25.00,
            status='PENDING'
        )
        
        self.assertEqual(reservation.user.email, 'client@example.com')
        self.assertEqual(reservation.court.name, 'Terrain 1')
        self.assertEqual(reservation.status, 'PENDING')
    
    def test_can_cancel_reservation(self):
        """Tester si une réservation peut être annulée (24h avant)."""
        # Réservation dans plus de 24h
        start = timezone.now() + timedelta(hours=25)
        end = start + timedelta(hours=1)
        
        reservation = Reservation.objects.create(
            user=self.client,
            court=self.court,
            start_datetime=start,
            end_datetime=end,
            price_per_hour=25.00,
            total_amount=25.00,
            status='CONFIRMED'
        )
        
        self.assertTrue(reservation.can_be_cancelled())
    
    def test_cannot_cancel_late_reservation(self):
        """Tester qu'on ne peut pas annuler une réservation < 24h."""
        # Réservation dans 12h
        start = timezone.now() + timedelta(hours=12)
        end = start + timedelta(hours=1)
        
        reservation = Reservation.objects.create(
            user=self.client,
            court=self.court,
            start_datetime=start,
            end_datetime=end,
            price_per_hour=25.00,
            total_amount=25.00,
            status='CONFIRMED'
        )
        
        self.assertFalse(reservation.can_be_cancelled())
