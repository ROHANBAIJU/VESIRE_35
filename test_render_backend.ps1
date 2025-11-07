# PowerShell script to test Render backend API
# Run this to check if your backend is working

$RENDER_URL = "https://vesire-35.onrender.com"
$API_URL = "$RENDER_URL/api"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🧪 Testing AgriScan Render Backend" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Base URL
Write-Host "Test 1: Base URL Reachability" -ForegroundColor Yellow
Write-Host "URL: $RENDER_URL" -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri $RENDER_URL -Method GET -TimeoutSec 10
    Write-Host "✅ PASSED - Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ FAILED - Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Health Check
Write-Host "Test 2: Health Check Endpoint" -ForegroundColor Yellow
Write-Host "URL: $API_URL/health" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$API_URL/health" -Method GET -TimeoutSec 10
    Write-Host "✅ PASSED - Status: $($response.status)" -ForegroundColor Green
    Write-Host "   Model Loaded: $($response.model_loaded)" -ForegroundColor Gray
    Write-Host "   Version: $($response.version)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED - Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: API Info
Write-Host "Test 3: API Info Endpoint" -ForegroundColor Yellow
Write-Host "URL: $API_URL/info" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$API_URL/info" -Method GET -TimeoutSec 10
    Write-Host "✅ PASSED" -ForegroundColor Green
    Write-Host "   API: $($response.name)" -ForegroundColor Gray
    Write-Host "   Version: $($response.version)" -ForegroundColor Gray
    Write-Host "   Model Loaded: $($response.model_info.loaded)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED - Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Models Info
Write-Host "Test 4: Models Info Endpoint" -ForegroundColor Yellow
Write-Host "URL: $API_URL/models" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$API_URL/models" -Method GET -TimeoutSec 10
    Write-Host "✅ PASSED" -ForegroundColor Green
    Write-Host "   Model Loaded: $($response.loaded)" -ForegroundColor Gray
    Write-Host "   Classes: $($response.num_classes)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED - Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 5: Diagnose Endpoint (RAG)
Write-Host "Test 5: RAG Diagnosis Endpoint (Critical for Gemini)" -ForegroundColor Yellow
$testDisease = "Tomato leaf late blight"
Write-Host "URL: $API_URL/diagnose/$testDisease" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$API_URL/diagnose/$([System.Uri]::EscapeDataString($testDisease))?language=en" -Method GET -TimeoutSec 30
    if ($response.success -eq $true) {
        Write-Host "✅ PASSED - RAG is working!" -ForegroundColor Green
        Write-Host "   Source: $($response.source)" -ForegroundColor Gray
        Write-Host "   Disease Found: $($response.disease -ne $null)" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  WARNING - Endpoint works but no diagnosis" -ForegroundColor Yellow
        Write-Host "   Error: $($response.error)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ FAILED - RAG not working" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   This usually means:" -ForegroundColor Yellow
    Write-Host "   - GEMINI_API_KEY not set in Render" -ForegroundColor Yellow
    Write-Host "   - Backend timeout (30s)" -ForegroundColor Yellow
    Write-Host "   - Knowledge base missing" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Test Complete!" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If RAG diagnosis failed, check:" -ForegroundColor Yellow
Write-Host "1. Render Dashboard → Environment Variables → GEMINI_API_KEY" -ForegroundColor White
Write-Host "2. Backend logs in Render dashboard" -ForegroundColor White
Write-Host "3. Try running: flutter run" -ForegroundColor White
Write-Host "   Then tap the API icon (top right) in the app" -ForegroundColor White
