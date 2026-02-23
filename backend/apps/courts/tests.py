"""
Tests pour les modèles de terrains.
"""

from django.test import TestCase
from apps.auth_app.models import Role, CustomUser
from apps.sites.models import Site
from apps.courts.models import Court, Equipment


class CourtTestCase(TestCase):
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
        
        self.court = Court.objects.create(
            name='Terrain 1',
            sport_type='TENNIS',
            site=self.site,
            price_per_hour=25.00,
            capacity=2
        )
    
    def test_court_creation(self):
        """Tester la création d'un terrain."""
        self.assertEqual(self.court.name, 'Terrain 1')
        self.assertEqual(self.court.sport_type, 'TENNIS')
        self.assertEqual(self.court.price_per_hour, 25.00)
    
    def test_court_equipments(self):
        """Tester l'ajout d'équipements à un terrain."""
        equipment = Equipment.objects.create(name='Éclairage')
        self.court.equipments.add(equipment)
        
        self.assertIn(equipment, self.court.equipments.all())
    
    def test_court_string_representation(self):
        """Tester la représentation en string du terrain."""
        self.assertEqual(str(self.court), 'Terrain 1 (Tennis)')
