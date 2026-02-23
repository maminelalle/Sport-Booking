#!/usr/bin/env python3
"""
Script complet de lancement du projet SportBooking
- Initialise la base de données
- Lance les serveurs (Backend + Frontend)
- Configure tout automatiquement
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def run_command(cmd, cwd=None, description="", bg=False):
    """Exécute une commande."""
    print(f"\n{'='*70}")
    print(f"▶️  {description}")
    print(f"{'='*70}")
    
    try:
        if bg:
            # Lancer en arrière-plan
            process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"✅ Lancé en arrière-plan (PID: {process.pid})")
            return process
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd)
            if result.returncode == 0:
                print(f"✅ Succès: {description}")
                return True
            else:
                print(f"⚠️  Erreur: {description}")
                return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    """Fonction principale."""
    root_path = Path(__file__).parent
    backend_path = root_path / "backend"
    frontend_path = root_path / "frontend"
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        🎾 SPORTBOOKING - LANCEMENT COMPLET               ║
    ║      Backend Django + Frontend React + Intégration        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Vérifier que nous sommes au bon endroit
    if not backend_path.exists() or not frontend_path.exists():
        print("❌ Erreur: backend/ et frontend/ n'existent pas")
        sys.exit(1)
    
    processes = []
    
    try:
        # 1. Pré configurations
        print("\n📋 ÉTAPE 1: PRÉ-CONFIGURATION")
        print("="*70)
        
        # Vérifier Python
        py_cmd = sys.executable
        print(f"  ✅ Python: {py_cmd}")
        
        # 2. Backend Django
        print("\n📋 ÉTAPE 2: CONFIGURATION DJANGO BACKEND")
        print("="*70)
        
        # Migrations
        run_command(
            f'{py_cmd} manage.py migrate --run-syncdb',
            cwd=str(backend_path),
            description="Django: Migrations"
        )
        
        # Initialiser les données
        run_command(
            f'{py_cmd} init_data.py',
            cwd=str(backend_path),
            description="Django: Initialisation des données"
        )
        
        # 3. Frontend
        print("\n📋 ÉTAPE 3: CONFIGURATION REACT FRONTEND")
        print("="*70)
        
        run_command(
            'npm install',
            cwd=str(frontend_path),
            description="React: Installation des dépendances"
        )
        
        # 4. Démarrage des serveurs
        print("\n" + "="*70)
        print("🚀 ÉTAPE 4: LANCEMENT DES SERVEURS")
        print("="*70)
        
        # Django backend
        backend_process = run_command(
            f'{py_cmd} manage.py runserver 0.0.0.0:8000',
            cwd=str(backend_path),
            description="Django: Démarrage sur http://localhost:8000",
            bg=True
        )
        if backend_process:
            processes.append(('Django Backend', backend_process))
        
        time.sleep(2)
        
        # React frontend
        frontend_process = run_command(
            'npm start',
            cwd=str(frontend_path),
            description="React: Démarrage sur http://localhost:3000",
            bg=True
        )
        if frontend_process:
            processes.append(('React Frontend', frontend_process))
        
        # 5. Afficher les informations
        print("\n" + "="*70)
        print("✅ DÉMARRAGE RÉUSSI!")
        print("="*70)
        print("""
        📝 ACCÈS AU PROJET:
        
        🌐 Frontend React:
           URL: http://localhost:3000
           
        🔌 Backend API:
           URL: http://localhost:8000/api
           Admin: http://localhost:8000/admin
           Docs: http://localhost:8000/api/schema/swagger
           
        👤 IDENTIFIANTS DE TEST:
        
           Admin:
           Email: admin@sportbooking.com
           Password: admin123456
           
           Manager:
           Email: manager@sportbooking.com
           Password: manager123456
           
           Client:
           Email: client@sportbooking.com
           Password: client123456
           
        💡 PROCHAINES ÉTAPES:
        
        1. Ouvrir http://localhost:3000 dans le navigateur
        2. Essayer la recherche de terrains
        3. Consulter les réservations
        4. Accéder à l'admin: http://localhost:8000/admin
        
        ⚠️  POUR ARRÊTER:
        Appuyez sur Ctrl+C
        """)
        
        # Garder les processus actifs
        print("\n🔄 Serveurs actifs. Appuyez sur Ctrl+C pour arrêter...\n")
        for name, process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print("\n\n⛔ Arrêt des serveurs...")
        for name, process in processes:
            try:
                process.terminate()
                print(f"  ✅ {name} arrêté")
            except:
                pass
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
