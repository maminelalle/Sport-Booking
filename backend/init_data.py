#!/usr/bin/env python
"""
Script d'initialisation complète du projet SportBooking.
Crée les données d'exemple et les utilisateurs de test.
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsbooking.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from django.contrib.auth.models import Group, Permission
from apps.auth_app.models import Role, CustomUser
from apps.sites.models import Site, OpeningHours
from apps.courts.models import Court, Equipment
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


def create_roles():
    """Crée les rôles de base."""
    print("📝 Création des rôles...")
    
    roles = [
        ('CLIENT', 'Client'),
        ('MANAGER', 'Gestionnaire'),
        ('ADMIN', 'Administrateur'),
    ]
    
    for name, description in roles:
        role, created = Role.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        status = "✅ Créé" if created else "⏭️  Déjà existant"
        print(f"  {status}: {name}")
    
    return Role.objects.all()


def create_users():
    """Crée les utilisateurs de test."""
    print("\n👤 Création des utilisateurs de test...")
    
    users = [
        {
            'username': 'admin',
            'email': 'admin@sportbooking.com',
            'password': 'admin123456',
            'is_staff': True,
            'is_superuser': True,
            'role_name': 'ADMIN',
            'first_name': 'Admin'
        },
        {
            'username': 'manager1',
            'email': 'manager@sportbooking.com',
            'password': 'manager123456',
            'is_staff': False,
            'is_superuser': False,
            'role_name': 'MANAGER',
            'first_name': 'Mohammed'
        },
        {
            'username': 'manager2',
            'email': 'manager2@sportbooking.com',
            'password': 'manager123456',
            'is_staff': False,
            'is_superuser': False,
            'role_name': 'MANAGER',
            'first_name': 'Hassan'
        },
        {
            'username': 'client1',
            'email': 'client1@sportbooking.com',
            'password': 'client123456',
            'is_staff': False,
            'is_superuser': False,
            'role_name': 'CLIENT',
            'first_name': 'Ahmed'
        },
        {
            'username': 'client2',
            'email': 'client2@sportbooking.com',
            'password': 'client123456',
            'is_staff': False,
            'is_superuser': False,
            'role_name': 'CLIENT',
            'first_name': 'Fatima'
        },
        {
            'username': 'client3',
            'email': 'client3@sportbooking.com',
            'password': 'client123456',
            'is_staff': False,
            'is_superuser': False,
            'role_name': 'CLIENT',
            'first_name': 'Ibrahim'
        },
        {
            'username': 'client4',
            'email': 'client4@sportbooking.com',
            'password': 'client123456',
            'is_staff': False,
            'is_superuser': False,
            'role_name': 'CLIENT',
            'first_name': 'Mariam'
        },
        {
            'username': 'client5',
            'email': 'client5@sportbooking.com',
            'password': 'client123456',
            'is_staff': False,
            'is_superuser': False,
            'role_name': 'CLIENT',
            'first_name': 'Omar'
        }
    ]
    
    for user_data in users:
        role = Role.objects.get(name=user_data['role_name'])
        
        user, created = CustomUser.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'is_staff': user_data['is_staff'],
                'is_superuser': user_data['is_superuser'],
                'first_name': user_data['first_name'],
                'role': role,
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"  ✅ Créé: {user_data['username']} ({user_data['email']})")
        else:
            print(f"  ⏭️  Déjà existant: {user_data['username']}")
    
    return CustomUser.objects.all()


def create_sites():
    """Crée les sites (lieux) d'exemple."""
    print("\n🏢 Création des sites de test...")
    
    # Get the manager user
    managers = CustomUser.objects.filter(role__name='MANAGER')
    manager1 = managers.first()
    manager2 = managers.last() if managers.count() > 1 else manager1
    
    sites = [
        {
            'name': 'Stade Omnisports Central Nouakchott',
            'description': 'Complexe sportif de classe mondiale avec installations couvertes et découvertes',
            'city': 'Nouakchott',
            'address': 'Avenue du 20 Août, Nouakchott',
            'postal_code': '00000',
            'latitude': 18.0735,
            'longitude': -15.9582,
            'manager_id': manager1.id if manager1 else 1,
        },
        {
            'name': 'Club Sportif Kiffa',
            'description': 'Installation moderne avec terrains de football professionnels climatisés',
            'city': ' Kiffa',
            'address': 'Route de Kiffa, Région de l\'Assaba',
            'postal_code': '22000',
            'latitude': 16.5833,
            'longitude': -11.4333,
            'manager_id': manager2.id if manager2 else 1,
        },
        {
            'name': 'Académie Sportive Rosso',
            'description': 'Centre d\'entraînement réputé pour le football et le handball',
            'city': 'Rosso',
            'address': 'Rue de l\'Académie, Rosso',
            'postal_code': '44000',
            'latitude': 16.5167,
            'longitude': -14.7833,
            'manager_id': manager1.id if manager1 else 1,
        },
        {
            'name': 'Centre Multisports Kaédi',
            'description': 'Complexe sportif complet avec 8 terrains couverts et équipements modernes',
            'city': 'Kaédi',
            'address': 'Boulevard Principal, Kaédi',
            'postal_code': '33000',
            'latitude': 16.1667,
            'longitude': -13.9667,
            'manager_id': manager2.id if manager2 else 1,
        },
        {
            'name': 'Stade Arafat Nouadhibou',
            'description': 'Installation côtière avec excellente vue, terrains de haut niveau',
            'city': 'Nouadhibou',
            'address': 'Avenue de la Plage, Nouadhibou',
            'postal_code': '55000',
            'latitude': 20.9311,
            'longitude': -17.0381,
            'manager_id': manager1.id if manager1 else 1,
        },
        {
            'name': 'Sports Club Tidjikja',
            'description': 'Centre d\'entraînement professionnel au cœur du désert',
            'city': 'Tidjikja',
            'address': 'Centre Ville, Tidjikja',
            'postal_code': '66000',
            'latitude': 18.5559,
            'longitude': -11.4081,
            'manager_id': manager2.id if manager2 else 1,
        }
    ]
    
    for site_data in sites:
        site, created = Site.objects.get_or_create(
            name=site_data['name'],
            defaults=site_data
        )
        status = "✅ Créé" if created else "⏭️  Déjà existant"
        print(f"  {status}: {site_data['name']}")
    
    return Site.objects.all()


def create_courts():
    """Crée les terrains de test."""
    print("\n🎾 Création des terrains de test...")
    
    sites = Site.objects.all()
    
    courts_template = [
        {'name': 'Terrain de Football Couvert 1', 'sport_type': 'FOOTBALL', 'price_per_hour': 75.00},
        {'name': 'Terrain de Football Couvert 2', 'sport_type': 'FOOTBALL', 'price_per_hour': 75.00},
        {'name': 'Court de Tennis Professionnel', 'sport_type': 'TENNIS', 'price_per_hour': 65.00},
        {'name': 'Terrain de Basketball Indoor', 'sport_type': 'BASKETBALL', 'price_per_hour': 60.00},
        {'name': 'Terrain de Volleyball', 'sport_type': 'VOLLEYBALL', 'price_per_hour': 55.00},
    ]
    
    count = 0
    for site in sites:
        for template in courts_template:
            name = f"{template['name']} - {site.name}"
            court, created = Court.objects.get_or_create(
                name=name,
                site=site,
                defaults={
                    'sport_type': template['sport_type'],
                    'capacity': 10,
                    'price_per_hour': template['price_per_hour'],
                    'description': f"Terrain professionnel {template['name'].lower()} - Équipements modernes et climatisation",
                }
            )
            if created:
                count += 1
                print(f"  ✅ Créé: {name}")
    
    print(f"  Total: {count} nouveaux terrains créés")
    print(f"  Total existant: {Court.objects.count()} terrains")


def create_equipment():
    """Crée les équipements."""
    print("\n⚽ Création des équipements...")
    
    equipment_types = [
        ('Ballon de Football', 'Ballon FIFA officiel de haute qualité'),
        ('Ballon de Tennis', 'Ballon de tennis professionnel'),
        ('Ballon de Basketball', 'Ballon NBA réglementaire'),
        ('Ballon de Volleyball', 'Ballon de volleyball international'),
        ('Filet de Football', 'Filet professionnel de haute résistance'),
        ('Raquette de Tennis', 'Raquette de tennis de compétition'),
        ('Chaussures de Sport', 'Chaussures de sport professionnelles'),
        ('Cônes d\'entraînement', 'Cônes plastique pour entraînement'),
        ('Gilets d\'entraînement', 'Gilets réversibles pour équipes'),
        ('Coussinets de Protection', 'Protection genoux et coudes'),
    ]
    
    count = 0
    for name, description in equipment_types:
        equip, created = Equipment.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if created:
            count += 1
            print(f"  ✅ Créé: {name}")
        else:
            print(f"  ⏭️  Déjà existant: {name}")
    
    print(f"  Total: {Equipment.objects.count()} équipements")


def show_summary():
    """Affiche un résumé des données créées."""
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES DONNÉES CRÉÉES")
    print("="*60)
    print(f"  👤 Utilisateurs: {CustomUser.objects.count()}")
    print(f"  🏢 Sites sportifs: {Site.objects.count()}")
    print(f"  🎾 Terrains disponibles: {Court.objects.count()}")
    print(f"  ⚽ Équipements: {Equipment.objects.count()}")
    print(f"  👨‍💼 Rôles: {Role.objects.count()}")
    print("="*60)
    print("\n✅ Initialisation terminée!")
    print("\n📝 Identifiants de connexion de test:")
    print("  Admin:")
    print("    Username: admin")
    print("    Password: admin123456")
    print("\n  Manager:")
    print("    Username: manager1 / manager2")
    print("    Password: manager123456")
    print("\n  Client:")
    print("    Username: client1 / client2 / client3 / client4 / client5")
    print("    Password: client123456")


def main():
    """Fonction principale."""
    try:
        print("""
        ╔════════════════════════════════════════════╗
        ║   🎾 INITIALISATION DES DONNÉES            ║
        ║   SportBooking Platform                    ║
        ╚════════════════════════════════════════════╝
        """)
        
        create_roles()
        create_users()
        create_sites()
        create_courts()
        create_equipment()
        show_summary()
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
