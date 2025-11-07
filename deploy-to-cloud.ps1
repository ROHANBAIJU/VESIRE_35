# Complete Deployment Script for Render + Netlify
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AgriScan Cloud Deployment" -ForegroundColor Cyan
Write-Host " Backend: Render | Frontend: Netlify" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build Flutter Web
Write-Host "STEP 1: Building Flutter Web..." -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Set-Location Z:\VESIRE_35\Frontend\vesire

flutter clean
flutter pub get
flutter build web --release

if ($LASTEXITCODE -ne 0) {
    Write-Host "Flutter build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Flutter web built successfully" -ForegroundColor Green
Write-Host ""

# Step 2: Commit and Push
Write-Host "STEP 2: Committing changes..." -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Set-Location Z:\VESIRE_35

git add -A
git add -f Frontend/vesire/build/web/*
git commit -m "deploy: pre-built Flutter web + flexible Python deps for cloud"
git push origin main

Write-Host "✅ Changes pushed to GitHub" -ForegroundColor Green
Write-Host ""

# Step 3: Instructions
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Deployment Triggered!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1️⃣  RENDER (Backend):" -ForegroundColor White
Write-Host "   🚨 CRITICAL: You MUST manually set Python version!" -ForegroundColor Red
Write-Host "   " -ForegroundColor White
Write-Host "   a) Go to: https://dashboard.render.com" -ForegroundColor Gray
Write-Host "   b) Click: agriscan-backend service" -ForegroundColor Gray
Write-Host "   c) Click: Settings > Environment" -ForegroundColor Gray
Write-Host "   d) Find: 'Python Version' dropdown" -ForegroundColor Gray
Write-Host "   e) Select: 3.11.6 (NOT 3.13!)" -ForegroundColor Yellow
Write-Host "   f) Click: Save Changes" -ForegroundColor Gray
Write-Host "   " -ForegroundColor White
Write-Host "   Build will start automatically" -ForegroundColor Gray
Write-Host "   Watch logs for: '==> Using Python version 3.11.6' ✅" -ForegroundColor Green
Write-Host ""

Write-Host "2️⃣  NETLIFY (Frontend):" -ForegroundColor White
Write-Host "   ✅ Pre-built files committed - will deploy automatically" -ForegroundColor Green
Write-Host "   " -ForegroundColor White
Write-Host "   a) Go to: https://app.netlify.com" -ForegroundColor Gray
Write-Host "   b) Check deploy status" -ForegroundColor Gray
Write-Host "   c) Should succeed now (using pre-built files)" -ForegroundColor Gray
Write-Host ""

Write-Host "3️⃣  AFTER SUCCESSFUL DEPLOY:" -ForegroundColor White
Write-Host "   a) Get Render URL: https://agriscan-backend-XXXX.onrender.com" -ForegroundColor Gray
Write-Host "   b) Update Frontend config:" -ForegroundColor Gray
Write-Host "      Edit: Frontend/vesire/lib/config/app_config.dart" -ForegroundColor Gray
Write-Host "      Set: _productionApiUrl = 'https://your-render-url.onrender.com/api'" -ForegroundColor Gray
Write-Host "   c) Rebuild Flutter and redeploy" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Monitor deployments:" -ForegroundColor Yellow
Write-Host "  Render: https://dashboard.render.com" -ForegroundColor Gray
Write-Host "  Netlify: https://app.netlify.com" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to open Render dashboard"
Start-Process "https://dashboard.render.com"

Read-Host "Press Enter to open Netlify dashboard"
Start-Process "https://app.netlify.com"
