"""
Tests pour les modèles d'sites.
"""

from django.test import TestCase
from apps.auth_app.models import Role, CustomUser
from apps.sites.models import Site, OpeningHours


class SiteTestCase(TestCase):
    def setUp(self):
        manager_role = Role.objects.create(name='MANAGER')
        
        self.manager = CustomUser.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password',
            role=manager_role
        )
        
        self.site = Site.objects.create(
            name='Centre Sportif Paris',
            address='123 Rue de Paris',
            city='Paris',
            postal_code='75001',
            latitude=48.8566,
            longitude=2.3522,
            manager=self.manager
        )
    
    def test_site_creation(self):
        """Tester la création d'un site."""
        self.assertEqual(self.site.name, 'Centre Sportif Paris')
        self.assertEqual(self.site.city, 'Paris')
        self.assertEqual(self.site.manager.email, 'manager@example.com')
    
    def test_opening_hours_creation(self):
        """Tester la création des horaires d'ouverture."""
        hours = OpeningHours.objects.create(
            site=self.site,
            day_of_week=0,  # Lundi
            open_time='08:00:00',
            close_time='22:00:00'
        )
        
        self.assertEqual(hours.day_of_week, 0)
        self.assertEqual(str(hours.open_time), '08:00:00')
    
    def test_site_string_representation(self):
        """Tester la représentation en string du site."""
        self.assertEqual(str(self.site), 'Centre Sportif Paris')
