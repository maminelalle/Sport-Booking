"""
Django commands pour initialiser les données du système.
"""

from django.core.management.base import BaseCommand
from apps.auth_app.models import Role, CustomUser
from apps.courts.models import Equipment


class Command(BaseCommand):
    help = 'Initialise les données de base du système'

    def handle(self, *args, **options):
        # Créer les rôles
        roles = [
            ('CLIENT', 'Client'),
            ('MANAGER', 'Gestionnaire de site'),
            ('ADMIN', 'Administrateur'),
        ]
        
        for name, description in roles:
            role, created = Role.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            status = "créé" if created else "existant"
            self.stdout.write(self.style.SUCCESS(f'Rôle {name} ({status})'))
        
        # Créer les équipements par défaut
        equipments = [
            ('Éclairage', 'Terrain éclairé'),
            ('Climatisation', 'Salle climatisée'),
            ('Vestiaires', 'Vestiaires disponibles'),
            ('Douches', 'Douches disponibles'),
            ('Parking', 'Parking disponible'),
            ('WiFi', 'WiFi gratuit'),
            ('Bar/Café', 'Bar/Café sur place'),
            ('Équipements fournis', 'Raquettes et balles fournis'),
            ('Spectateurs', 'Zones pour spectateurs'),
            ('Équipe médicale', 'Équipe médicale disponible'),
        ]
        
        for name, description in equipments:
            equipment, created = Equipment.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            status = "créé" if created else "existant"
            self.stdout.write(self.style.SUCCESS(f'Équipement {name} ({status})'))
        
        # Créer un administrateur par défaut (optionnel)
        admin_role = Role.objects.get(name='ADMIN')
        try:
            admin_user = CustomUser.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('Administrateur "admin" existe déjà'))
        except CustomUser.DoesNotExist:
            admin_user = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@sportsbooking.local',
                password='admin123',
                role=admin_role
            )
            self.stdout.write(self.style.SUCCESS('Administrateur par défaut créé'))
            self.stdout.write(self.style.WARNING('⚠️  IMPORTANT: Changez le mot de passe admin en production!'))
        
        self.stdout.write(self.style.SUCCESS('Initialisation complète'))
