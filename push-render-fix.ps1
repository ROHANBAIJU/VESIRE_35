# RENDER FIX - Push Updated Requirements
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " RENDER FIX - Push Updated Requirements" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location Z:\VESIRE_35

Write-Host "Step 1: Adding updated files..." -ForegroundColor Yellow
git add Backend/requirements.txt PYTHON_VERSION_FIX.md RENDER_FIX_GUIDE.md render.yaml CLOUD_DEPLOYMENT_GUIDE.md

Write-Host ""
Write-Host "Step 2: Committing changes..." -ForegroundColor Yellow
git commit -m "fix: update Pillow 10.3.0 and add Python 3.11 enforcement"

Write-Host ""
Write-Host "Step 3: Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Push Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🚨 CRITICAL: Now do this in Render Dashboard:" -ForegroundColor Red
Write-Host ""
Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Click your service: agriscan-backend" -ForegroundColor White
Write-Host "3. Click 'Settings' (left sidebar)" -ForegroundColor White
Write-Host "4. Scroll to 'Environment' section" -ForegroundColor White
Write-Host "5. Find 'Python Version' dropdown" -ForegroundColor White
Write-Host "6. Click dropdown and select: 3.11.6" -ForegroundColor Yellow
Write-Host "7. Click 'Save Changes'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Then watch build logs for:" -ForegroundColor Cyan
Write-Host "  '==> Using Python version 3.11.6' ✅" -ForegroundColor Green
Write-Host ""
Write-Host "NOT:" -ForegroundColor Cyan
Write-Host "  '==> Using Python version 3.13.4' ❌" -ForegroundColor Red
Write-Host ""
Read-Host "Press Enter to continue"
