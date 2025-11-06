# Test Cloud Deployment Script
# Run this to verify your cloud deployment is working

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "☁️  AgriScan Cloud Deployment Test" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Configuration
$BACKEND_URL = "https://agriscan-backend.onrender.com"  # UPDATE THIS after deploying to Render
$FRONTEND_URL = "https://your-app.netlify.app"  # UPDATE THIS after deploying to Netlify

Write-Host "Testing Backend at: $BACKEND_URL" -ForegroundColor Yellow
Write-Host ""

# Test 1: Health Check
Write-Host "1️⃣  Testing health endpoint..." -ForegroundColor Blue
try {
    $health = Invoke-RestMethod -Uri "$BACKEND_URL/api/health" -Method Get -ErrorAction Stop
    Write-Host "   ✅ Backend is healthy!" -ForegroundColor Green
    Write-Host "   Model loaded: $($health.model_loaded)" -ForegroundColor White
    Write-Host "   Version: $($health.version)" -ForegroundColor White
} catch {
    Write-Host "   ❌ Backend health check failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 2: Multilingual RAG (Hindi)
Write-Host "2️⃣  Testing multilingual RAG (Hindi)..." -ForegroundColor Blue
try {
    $diagnosis = Invoke-RestMethod -Uri "$BACKEND_URL/api/diagnose/Tomato%20leaf%20late%20blight?language=hi&use_cache=false" -Method Get -TimeoutSec 60 -ErrorAction Stop
    
    if ($diagnosis.success) {
        Write-Host "   ✅ RAG working! Source: $($diagnosis.source)" -ForegroundColor Green
        
        $description = $diagnosis.disease.description
        $hasHindi = $description -match '[\u0900-\u097F]'
        
        if ($hasHindi) {
            Write-Host "   ✅ Hindi script detected!" -ForegroundColor Green
            Write-Host "   Description preview: $($description.Substring(0, [Math]::Min(100, $description.Length)))..." -ForegroundColor White
        } else {
            Write-Host "   ⚠️  No Hindi script detected in response" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ❌ RAG request failed: $($diagnosis.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ RAG test failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Frontend Accessibility
Write-Host "3️⃣  Testing frontend accessibility..." -ForegroundColor Blue
if ($FRONTEND_URL -ne "https://your-app.netlify.app") {
    try {
        $response = Invoke-WebRequest -Uri $FRONTEND_URL -Method Get -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ Frontend is accessible!" -ForegroundColor Green
            Write-Host "   Opening in browser..." -ForegroundColor Yellow
            Start-Process $FRONTEND_URL
        }
    } catch {
        Write-Host "   ❌ Frontend not accessible!" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "   ⚠️  Update FRONTEND_URL in this script with your Netlify URL" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Cloud deployment test complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update backend URL in Frontend/vesire/lib/config/app_config.dart" -ForegroundColor White
Write-Host "2. Rebuild Flutter web: flutter build web --release" -ForegroundColor White
Write-Host "3. Deploy to Netlify" -ForegroundColor White
Write-Host "4. Test end-to-end with mobile app`n" -ForegroundColor White
