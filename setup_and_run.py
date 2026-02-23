#!/usr/bin/env python
"""
Script de configuration et démarrage complet du projet SportBooking.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, description=""):
    """Exécute une commande et affiche le résultat."""
    print(f"\n{'='*60}")
    print(f"▶️  {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=False)
        if result.returncode != 0:
            print(f"⚠️  Erreur lors de: {description}")
            return False
        print(f"✅ {description} - OK")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def setup_backend():
    """Configure et prépare le backend Django."""
    backend_path = Path(__file__).parent / "backend"
    
    print("\n" + "="*60)
    print("🔧 CONFIGURATION DU BACKEND DJANGO")
    print("="*60)
    
    # Créer les répertoires migrations s'ils n'existent pas
    for app in ["core", "auth_app", "sites", "courts", "reservations", "payments"]:
        migrations_dir = backend_path / "apps" / app / "migrations"
        if not migrations_dir.exists():
            print(f"  📁 Création {app}/migrations/")
            migrations_dir.mkdir(parents=True, exist_ok=True)
            (migrations_dir / "__init__.py").touch()
    
    # Faire les migrations
    run_command(
        f"{sys.executable} manage.py makemigrations",
        cwd=str(backend_path),
        description="Django makemigrations"
    )
    
    # Appliquer les migrations
    run_command(
        f"{sys.executable} manage.py migrate --run-syncdb",
        cwd=str(backend_path),
        description="Django migrate"
    )
    
    # Créer un utilisateur admin (optionnel)
    print("\n  💡 Pour créer un utilisateur admin, exécutez:")
    print("     python manage.py createsuperuser")

def setup_frontend():
    """Configure et prépare le frontend React."""
    frontend_path = Path(__file__).parent / "frontend"
    
    print("\n" + "="*60)
    print("🎨 CONFIGURATION DU FRONTEND REACT")
    print("="*60)
    
    # Installer les dépendances
    run_command(
        "npm install",
        cwd=str(frontend_path),
        description="NPM install dependencies"
    )

def create_sample_data():
    """Crée les données d'exemple."""
    backend_path = Path(__file__).parent / "backend"
    
    print("\n" + "="*60)
    print("🌱 CRÉATION DES DONNÉES D'EXEMPLE")
    print("="*60)
    
    run_command(
        f"{sys.executable} manage.py initialize_data",
        cwd=str(backend_path),
        description="Création des données d'exemple"
    )

def main():
    """Fonction principale."""
    print("""
    ╔════════════════════════════════════════════╗
    ║   🎾 SPORTBOOKING PLATFORM SETUP          ║
    ║   Configuration et Démarrage Complet      ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Erreur: Exécutez ce script depuis la racine du projet")
        sys.exit(1)
    
    # Setup backend
    setup_backend()
    
    # Setup frontend
    setup_frontend()
    
    # Créer les données d'exemple
    # create_sample_data()  # Décommenter si vous avez la migration
    
    print("\n" + "="*60)
    print("✅ CONFIGURATION TERMINÉE!")
    print("="*60)
    print("""
    📝 PROCHAINES ÉTAPES:
    
    1️⃣  Pour démarrer les serveurs:
        • Backend:  cd backend && python manage.py runserver
        • Frontend: cd frontend && npm start
        
    2️⃣  Accédez à l'application:
        • Frontend: http://localhost:3000
        • Backend:  http://localhost:8000
        • Admin:    http://localhost:8000/admin
        
    3️⃣  Pour créer un utilisateur admin:
        cd backend && python manage.py createsuperuser
        
    4️⃣  Variables d'environnement (.env):
        - SECRET_KEY (Django)
        - STRIPE_PUBLIC_KEY
        - STRIPE_SECRET_KEY
        - CORS_ALLOWED_ORIGINS
    """)

if __name__ == "__main__":
    main()
