# Build and Deploy Flutter Web to Netlify
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Flutter Web Build for Netlify" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location Z:\VESIRE_35\Frontend\vesire

Write-Host "Step 1: Clean previous build..." -ForegroundColor Yellow
flutter clean

Write-Host ""
Write-Host "Step 2: Get dependencies..." -ForegroundColor Yellow
flutter pub get

Write-Host ""
Write-Host "Step 3: Building Flutter web (Release mode)..." -ForegroundColor Yellow
Write-Host "This may take 2-3 minutes..." -ForegroundColor Gray
flutter build web --release --web-renderer canvaskit

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " Build Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Build output: Frontend/vesire/build/web" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Commit the build/web folder:" -ForegroundColor White
    Write-Host "   cd Z:\VESIRE_35" -ForegroundColor Gray
    Write-Host "   git add Frontend/vesire/build/web" -ForegroundColor Gray
    Write-Host "   git add netlify.toml Backend/requirements.txt" -ForegroundColor Gray
    Write-Host "   git commit -m 'feat: add pre-built Flutter web for Netlify'" -ForegroundColor Gray
    Write-Host "   git push origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Netlify will automatically deploy the pre-built files!" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host " Build Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above." -ForegroundColor Yellow
}

Read-Host "Press Enter to continue"
