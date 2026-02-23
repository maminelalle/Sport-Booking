@echo off
REM ==========================================
REM SportBook - Démarrage Complet
REM ==========================================

echo.
echo ╔════════════════════════════════════════╗
echo ║   🎾 SPORTBOOK - DEMARRAGE COMPLET    ║
echo ╚════════════════════════════════════════╝
echo.

REM Chemins vers Python et Node
set PYTHON=.venv\Scripts\python.exe
set NPM=npm

REM Vérifier que nous sommes au bon endroit
if not exist "backend\" (
    echo ❌ Erreur: backend/ non trouvé
    pause
    exit /b 1
)

if not exist "frontend\" (
    echo ❌ Erreur: frontend/ non trouvé
    pause
    exit /b 1
)

echo 📋 Préparation du Backend...
echo.

REM Backend setup
cd backend

echo Running migrations...
%PYTHON% manage.py migrate --run-syncdb 2>nul

echo Creating test data...
%PYTHON% init_data.py 2>nul

cd ..

echo.
echo 🚀 Démarrage des serveurs...
echo.

REM Démarrer Django
echo Démarrage Django Backend sur http://localhost:8000
start cmd /title "Django Backend" /k "%PYTHON% backend\manage.py runserver 0.0.0.0:8000"

REM Attendre
timeout /t 3 /nobreak

REM Démarrer React
echo Démarrage React Frontend sur http://localhost:3000
start cmd /title "React Frontend" /k "cd frontend && npm start"

echo.
echo ╔════════════════════════════════════════╗
echo ║   ✅ SERVEURS LANCÉS                  ║
echo ╠════════════════════════════════════════╣
echo ║   Frontend: http://localhost:3000     ║
echo ║   Backend: http://localhost:8000/api  ║
echo ║   Admin: http://localhost:8000/admin  ║
echo ╠════════════════════════════════════════╣
echo ║   Email: admin@sportbooking.com       ║
echo ║   Pass: admin123456                   ║
echo ╚════════════════════════════════════════╝
echo.
pause
