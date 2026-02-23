@echo off
REM Script de démarrage simple pour SportBooking
REM Lance Django Backend et React Frontend

echo.
echo ╔════════════════════════════════════════════╗
echo ║   🎾 SPORTBOOKING - DÉMARRAGE             ║
echo ║   Backend Django + Frontend React         ║
echo ╚════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

REM Vérifier les répertoires
if not exist "backend\" (
    echo ❌ Erreur: répertoire 'backend' non trouvé
    pause
    exit /b 1
)

if not exist "frontend\" (
    echo ❌ Erreur: répertoire 'frontend' non trouvé
    pause
    exit /b 1
)

REM Initialiser le backend
echo.
echo 📋 INITIALISATION DU BACKEND...
echo.

cd backend

echo Running migrations...
python manage.py migrate --run-syncdb

echo Initializing data...
python manage.py init_data.py 2>nul

cd ..

REM Démarrer les serveurs
echo.
echo 🚀 DÉMARRAGE DES SERVEURS...
echo.

REM Fenêtre 1: Django
start cmd /title "Django Backend - http://localhost:8000" /k "cd backend && python manage.py runserver 0.0.0.0:8000"

REM Attendre 2 secondes
timeout /t 2 /nobreak

REM Fenêtre 2: React
start cmd /title "React Frontend - http://localhost:3000" /k "cd frontend && npm start"

REM Afficher les instructions
echo.
echo ╔════════════════════════════════════════════╗
echo ║   ✅ SERVEURS LANCÉS                      ║
echo ╠════════════════════════════════════════════╣
echo ║   🌐 Frontend: http://localhost:3000      ║
echo ║   🔌 Backend: http://localhost:8000/api   ║
echo ║   👨‍💼 Admin: http://localhost:8000/admin    ║
echo ╚════════════════════════════════════════════╝
echo.
echo.
echo 📝 IDENTIFIANTS DE TEST:
echo    Admin / admin@sportbooking.com / admin123456
echo    Manager / manager@sportbooking.com / manager123456
echo    Client / client@sportbooking.com / client123456
echo.

pause
