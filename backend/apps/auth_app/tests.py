"""
Tests pour les modèles d'authentification.
"""

from django.test import TestCase
from apps.auth_app.models import Role, CustomUser


class RoleTestCase(TestCase):
    def setUp(self):
        self.role = Role.objects.create(
            name='CLIENT',
            description='Client role'
        )
    
    def test_role_creation(self):
        """Tester la création d'un rôle."""
        self.assertEqual(self.role.name, 'CLIENT')
        self.assertEqual(self.role.description, 'Client role')
    
    def test_role_string_representation(self):
        """Tester la représentation en string du rôle."""
        self.assertEqual(str(self.role), 'Client')


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='CLIENT')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.role
        )
    
    def test_user_creation(self):
        """Tester la création d'un utilisateur."""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role.name, 'CLIENT')
    
    def test_user_password_hashing(self):
        """Tester que le mot de passe est hashé."""
        self.assertNotEqual(self.user.password, 'testpass123')
    
    def test_user_authentication(self):
        """Tester l'authentification de l'utilisateur."""
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.check_password('wrongpassword'))
