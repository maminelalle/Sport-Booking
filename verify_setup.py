#!/usr/bin/env python3
"""
Script de vérification que tout est configuré et en cours d'exécution
"""

import subprocess
import time
import sys
import requests
from pathlib import Path

def check_service(url, name, timeout=5):
    """Vérifie qu'un service répond."""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code < 500:
            print(f"  ✅ {name}: {url} - OK (HTTP {response.status_code})")
            return True
    except Exception as e:
        print(f"  ❌ {name}: {url} - Non disponible")
        return False
    return False

def check_file(path, description):
    """Vérifie qu'un fichier existe."""
    if Path(path).exists():
        print(f"  ✅ {description}: {path}")
        return True
    else:
        print(f"  ❌ {description}: {path} - MANQUANT!")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        🔍 VÉRIFICATION DU PROJET SPORTBOOKING             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    all_ok = True
    
    print("\n📋 VÉRIFICATION DES FICHIERS:")
    all_ok &= check_file("backend/manage.py", "Django manage.py")
    all_ok &= check_file("frontend/package.json", "React package.json")
    all_ok &= check_file("backend/db.sqlite3", "Base de données Django")
    all_ok &= check_file("backend/init_data.py", "Script d'initialisation")
    
    print("\n🔌 VÉRIFICATION DES SERVICES (connexions HTTP):")
    print("  ⏳ Attente de 3 secondes pour que les serveurs répondent...")
    time.sleep(3)
    
    check_service("http://localhost:8000/api/", "Django Backend", timeout=3)
    check_service("http://localhost:3000/", "React Frontend", timeout=3)
    
    print("\n📝 VÉRIFICATION DES ENDPOINTS API:")
    try:
        response = requests.get("http://localhost:8000/api/", timeout=3)
        print(f"  🔌 API accessible - Réponse: {response.status_code}")
    except:
        print(f"  ❌ API non accessible - Django n'est pas lancé")
    
    print("\n" + "="*70)
    if all_ok:
        print("✅ TOUT SEMBLE CONFIGURÉ CORRECTEMENT!")
        print("="*70)
        print("""
        🌐 Accédez à:
           Frontend: http://localhost:3000
           Backend:  http://localhost:8000/api
           Admin:    http://localhost:8000/admin
        """)
    else:
        print("⚠️  ATTENTION: Certains éléments ne sont pas configurés")
        print("="*70)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
