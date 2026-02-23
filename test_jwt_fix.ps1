# Script de test pour vérifier que le JWT fonctionne maintenant

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   TEST JWT - Vérification de l'authentification     ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

try {
    Write-Host "1️⃣  Connexion..." -ForegroundColor Yellow
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Body (@{
        email='client@sportbooking.com'
        password='client123456'
    } | ConvertTo-Json) -ContentType "application/json"
    
    $token = $loginResponse.access
    Write-Host "   ✅ Login réussi!" -ForegroundColor Green
    
    Write-Host "`n2️⃣  Test de l'authentification..." -ForegroundColor Yellow
    $auth = Invoke-RestMethod -Uri "http://localhost:8000/api/reservations/test_auth/" -Method GET -Headers @{
        Authorization="Bearer $token"
    }
    
    Write-Host "   ✅ Authentification réussie!" -ForegroundColor Green
    Write-Host "   User: $($auth.user_email)" -ForegroundColor White
    Write-Host "   ID: $($auth.user_id)" -ForegroundColor White
    Write-Host "   Role: $($auth.user_role)" -ForegroundColor White
    
    Write-Host "`n3️⃣  Récupération des réservations..." -ForegroundColor Yellow
    $reservations = Invoke-RestMethod -Uri "http://localhost:8000/api/reservations/" -Method GET -Headers @{
        Authorization="Bearer $token"
    }
    
    Write-Host "   ✅ Réservations récupérées: $($reservations.results.Count)" -ForegroundColor Green
    
    Write-Host "`n" -ForegroundColor Green
    Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║              ✨ TOUT FONCTIONNE! ✨                  ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host "`n"
    Write-Host "👉 Maintenant, allez dans votre navigateur:" -ForegroundColor Cyan
    Write-Host "   1. Ouvrez la console (F12)" -ForegroundColor White
    Write-Host "   2. Tapez: localStorage.clear()" -ForegroundColor White
    Write-Host "   3. Rechargez la page" -ForegroundColor White
    Write-Host "   4. Reconnectez-vous" -ForegroundColor White
    Write-Host "   5. Essayez de réserver un terrain ✅" -ForegroundColor White
    Write-Host "`n"
    
} catch {
    Write-Host "`n❌ ERREUR:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "`nAssurez-vous que le serveur backend est démarré (port 8000)" -ForegroundColor Yellow
}
