# AgriScan Flutter App Start Script
# This script runs the Flutter app

Write-Host "📱 Starting AgriScan Flutter App..." -ForegroundColor Green
Write-Host ""

# Navigate to frontend directory
$FrontendPath = "z:\VESIRE_35\Frontend\vesire"
Set-Location $FrontendPath

# Check if Flutter is installed
Write-Host "🔍 Checking Flutter installation..." -ForegroundColor Cyan
flutter --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Flutter not found! Please install Flutter first." -ForegroundColor Red
    Write-Host "   Download from: https://flutter.dev/docs/get-started/install" -ForegroundColor Yellow
    exit 1
}

# Get dependencies
Write-Host "📦 Getting Flutter dependencies..." -ForegroundColor Cyan
flutter pub get

Write-Host ""
Write-Host "✅ Starting Flutter App..." -ForegroundColor Green
Write-Host ""
Write-Host "📝 Make sure to:" -ForegroundColor Yellow
Write-Host "   1. Start the backend server first (run start_backend.ps1)" -ForegroundColor Gray
Write-Host "   2. Update API URL in lib/config/app_config.dart if using physical device" -ForegroundColor Gray
Write-Host "   3. Connect your device or start an emulator" -ForegroundColor Gray
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Run Flutter app
flutter run
