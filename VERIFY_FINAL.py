#!/usr/bin/env python3
"""
✅ VÉRIFICATION FINALE DU PROJET SPORTBOOK
Vérifie que tout est correct avant de démarrer
"""

import os
import sys
from pathlib import Path
import subprocess

def check_file(filepath, description=""):
    """Vérifie qu'un fichier existe."""
    path = Path(filepath)
    emoji = "✅" if path.exists() else "❌"
    status = "OK" if path.exists() else "MANQUANT"
    print(f"  {emoji} {description:<40} {status}")
    return path.exists()

def check_directory(dirpath, description=""):
    """Vérifie qu'un répertoire existe."""
    path = Path(dirpath)
    emoji = "✅" if path.exists() else "❌"
    status = "OK" if path.exists() else "MANQUANT"
    print(f"  {emoji} {description:<40} {status}")
    return path.exists()

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     🔍 VÉRIFICATION FINALE DU PROJET SPORTBOOK             ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    all_ok = True
    
    # Vérifier la structure du projet
    print("\n📂 STRUCTURE DU PROJET:")
    all_ok &= check_directory("backend", "Répertoire backend/")
    all_ok &= check_directory("frontend", "Répertoire frontend/")
    all_ok &= check_directory(".venv", "Virtual environment Python")
    
    # Vérifier les fichiers Django
    print("\n🔌 FICHIERS DJANGO:")
    all_ok &= check_file("backend/manage.py", "manage.py")
    all_ok &= check_file("backend/init_data.py", "init_data.py")
    all_ok &= check_file("backend/sportsbooking/settings.py", "settings.py")
    all_ok &= check_file("backend/sportsbooking/urls.py", "urls.py")
    all_ok &= check_file("backend/requirements.txt", "requirements.txt")
    
    # Vérifier les fichiers React
    print("\n⚛️  FICHIERS REACT:")
    all_ok &= check_file("frontend/package.json", "package.json")
    all_ok &= check_file("frontend/public/index.html", "index.html")
    all_ok &= check_file("frontend/src/App.js", "App.js")
    all_ok &= check_file("frontend/src/api/client.js", "API client")
    all_ok &= check_file("frontend/src/api/hooks.js", "API hooks")
    
    # Vérifier les pages React
    print("\n📄 PAGES REACT:")
    pages = [
        "HomePage.jsx",
        "SearchResultsPage.jsx",
        "CourtDetailsPage.jsx",
        "BookingPage.jsx",
        "DashboardPage.jsx"
    ]
    for page in pages:
        all_ok &= check_file(f"frontend/src/pages/{page}", f"  {page}")
    
    # Vérifier les fichiers de configuration
    print("\n⚙️  CONFIGURATION:")
    all_ok &= check_file(".env", ".env (racine)")
    all_ok &= check_file("frontend/.env", "frontend/.env")
    all_ok &= check_file("backend/db.sqlite3", "Base de données Django")
    
    # Vérifier les scripts de démarrage
    print("\n🚀 SCRIPTS DE DÉMARRAGE:")
    all_ok &= check_file("START.bat", "START.bat")
    all_ok &= check_file("run_complete.py", "run_complete.py")
    
    # Vérifier les fichiers d'apps Django
    print("\n🏗️  APPS DJANGO:")
    apps = ["auth_app", "courts", "sites", "reservations", "payments", "core"]
    for app in apps:
        all_ok &= check_directory(f"backend/apps/{app}", f"  {app}/")
    
    # Vérifier les fichiers de migration
    print("\n📊 MIGRATIONS:")
    for app in apps:
        migrations_dir = f"backend/apps/{app}/migrations"
        all_ok &= check_directory(migrations_dir, f"  {app}/migrations/")
    
    # Vérifier les composants
    print("\n🧩 COMPOSANTS REACT:")
    all_ok &= check_file("frontend/src/components/Navbar.jsx", "Navbar.jsx")
    
    # Vérifier les fichiers de documentation
    print("\n📚 DOCUMENTATION:")
    all_ok &= check_file("GUIDE_COMPLET.md", "GUIDE_COMPLET.md")
    all_ok &= check_file("FINAL_STATUS.md", "FINAL_STATUS.md")
    all_ok &= check_file("README.md", "README.md")
    
    # Résumé
    print("\n" + "="*70)
    if all_ok:
        print("✅ TOUT EST CORRECT!")
        print("="*70)
        print("""
        🎉 Le projet est prêt à démarrer!
        
        🚀 COMMENT DÉMARRER:
        
        Option 1 (Windows):
          • Double-cliquez sur START.bat
          
        Option 2 (Terminal):
          • python run_complete.py
          
        🌐 Accès:
        • Frontend: http://localhost:3000
        • Backend: http://localhost:8000/api
        • Admin: http://localhost:8000/admin
        
        👤 Connexion:
        • Email: admin@sportbooking.com
        • Mot de passe: admin123456
        """)
        return 0
    else:
        print("⚠️  ATTENTION: Certains fichiers sont manquants!")
        print("="*70)
        print("""
        Les fichiers ou répertoires suivants sont manquants:
        
        Actions correctrices:
        1. Vérifiez que vous êtes dans le bon répertoire
        2. Rédownloadez la structure complète si nécessaire
        3. Exécutez: python setup_and_run.py
        """)
        return 1

if __name__ == "__main__":
    sys.exit(main())
