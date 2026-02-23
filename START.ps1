# ==========================================
# SportBook - Démarrage Rapide (PowerShell)
# ==========================================

Write-Host @"
╔════════════════════════════════════════╗
║   🎾 SPORTBOOK - DÉMARRAGE RAPIDE     ║
╚════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Configuration
$PythonExe = ".\.venv\Scripts\python.exe"
$BackendDir = ".\backend"
$FrontendDir = ".\frontend"

# Vérifier les répertoires
if (-not (Test-Path $BackendDir)) {
    Write-Host "❌ Erreur: backend/ non trouvé" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $FrontendDir)) {
    Write-Host "❌ Erreur: frontend/ non trouvé" -ForegroundColor Red
    exit 1
}

# Configuration du Backend
Write-Host "`n📋 Configuration du Backend..." -ForegroundColor Yellow

Push-Location $BackendDir

Write-Host "  ▶ Migrations Django..."
& $PythonExe manage.py migrate --run-syncdb 2>$null

Write-Host "  ▶ Initialisation des données..."
& $PythonExe init_data.py 2>$null

Pop-Location

Write-Host "`n✅ Backend configuré!" -ForegroundColor Green

# Démarrage des serveurs
Write-Host "`n🚀 Démarrage des serveurs..." -ForegroundColor Yellow

Write-Host "`n  🔵 Django sur http://localhost:8000" -ForegroundColor Cyan
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; . `"$PythonExe`" manage.py runserver 0.0.0.0:8000"

Start-Sleep -Seconds 2

Write-Host "  🟢 React sur http://localhost:3000" -ForegroundColor Cyan
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd '$FrontendDir'; npm start"

Write-Host @"

╔════════════════════════════════════════╗
║   ✅ SERVEURS LANCÉS                  ║
╠════════════════════════════════════════╣
║   Frontend: http://localhost:3000     ║
║   Backend:  http://localhost:8000/api ║
║   Admin:    http://localhost:8000     ║
╠════════════════════════════════════════╣
║   Email: admin@sportbooking.com       ║
║   Pass: admin123456                   ║
╚════════════════════════════════════════╝
"@ -ForegroundColor Green

Write-Host "`n⏳ Attendez 30 secondes que les serveurs démarrent..."
Start-Sleep -Seconds 30

Write-Host "`n✨ Ouvrez le navigateur: http://localhost:3000`n" -ForegroundColor Green
