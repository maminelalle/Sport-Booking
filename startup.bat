@echo off
REM Startup Script for Windows - SportBooking Platform
REM Usage: startup.bat or startup.bat dev/prod

setlocal enabledelayedexpansion
set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=dev

echo ========================================
echo 🚀 SportBooking Platform Startup
echo Environment: %ENVIRONMENT%
echo ========================================
echo.

if "%ENVIRONMENT%"=="dev" (
    echo 📦 Installing dependencies...
    echo.
    
    REM Backend
    cd backend
    echo Installing Python dependencies...
    pip install -r requirements.txt
    
    echo Running migrations...
    python manage.py migrate
    
    echo Initializing data...
    python manage.py initialize_data
    
    cd ..
    REM Frontend
    cd frontend
    echo Installing Node dependencies...
    call npm install
    cd ..
    
    echo.
    echo ✅ Dependencies installed!
    echo.
    echo 🎯 Starting development servers...
    echo.
    echo Backend:  http://localhost:8000
    echo Frontend: http://localhost:3000
    echo API Docs: http://localhost:8000/api/schema/swagger/
    echo.
    echo Press Ctrl+C to stop the servers
    echo.
    
    REM Start Backend
    start cmd /k "cd backend && python manage.py runserver 0.0.0.0:8000"
    timeout /t 2 > nul
    
    REM Start Frontend
    start cmd /k "cd frontend && npm start"
    
) else if "%ENVIRONMENT%"=="prod" (
    echo 🐳 Starting production with Docker...
    echo.
    
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml up -d
    
    echo ✅ Production started!
    echo.
    echo Services:
    docker-compose -f docker-compose.prod.yml ps
    
) else if "%ENVIRONMENT%"=="docker" (
    echo 🐳 Starting with Docker Compose...
    docker-compose up
    
) else (
    echo Usage: startup.bat [dev^|prod^|docker]
    echo.
    echo Options:
    echo   dev    - Start development servers
    echo   prod   - Start production with Docker
    echo   docker - Start with Docker Compose
    exit /b 1
)

endlocal
