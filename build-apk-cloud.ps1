# Build AgriScan APK for Distribution
# Connects to Cloud Backend: https://vesire-35.onrender.com

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AgriScan APK Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location Z:\VESIRE_35\Frontend\vesire

Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
flutter clean
Write-Host "Clean complete" -ForegroundColor Green
Write-Host ""

Write-Host "Getting dependencies..." -ForegroundColor Yellow
flutter pub get
Write-Host "Dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "Generating app icons..." -ForegroundColor Yellow
dart run flutter_launcher_icons
Write-Host "App icons generated" -ForegroundColor Green
Write-Host ""

Write-Host "Building APK..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes..." -ForegroundColor Gray
Write-Host ""

flutter build apk --release

if ($LASTEXITCODE -ne 0) {
    Write-Host "APK build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "APK Built Successfully!" -ForegroundColor Green
Write-Host ""

$apkPath = "Z:\VESIRE_35\Frontend\vesire\build\app\outputs\flutter-apk\app-release.apk"
Write-Host "APK Location:" -ForegroundColor Yellow
Write-Host $apkPath -ForegroundColor White
Write-Host ""

if (Test-Path $apkPath) {
    $size = (Get-Item $apkPath).Length / 1MB
    Write-Host "APK Size: $([math]::Round($size, 2)) MB" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cloud Backend: https://vesire-35.onrender.com/api" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to open APK folder"
explorer.exe "Z:\VESIRE_35\Frontend\vesire\build\app\outputs\flutter-apk"
