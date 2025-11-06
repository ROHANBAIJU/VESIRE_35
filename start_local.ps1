# AgriScan Quick Start Script
# Run this to start both backend and frontend for local testing

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🚀 AgriScan Local Development Startup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if backend is already running
$backendRunning = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*VESIRE_35*"}

if ($backendRunning) {
    Write-Host "✅ Backend already running (PID: $($backendRunning.Id))" -ForegroundColor Green
} else {
    Write-Host "🔵 Starting Backend Server..." -ForegroundColor Blue
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Z:\VESIRE_35\Backend\api; python app.py" -WindowStyle Normal
    Write-Host "   Waiting 5 seconds for backend to initialize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    Write-Host "✅ Backend started at http://10.190.144.95:5000" -ForegroundColor Green
}

Write-Host "`n🟢 Starting Flutter Frontend..." -ForegroundColor Blue
Write-Host "   Choose your device:" -ForegroundColor Yellow
Write-Host "   1. Chrome (Web)" -ForegroundColor White
Write-Host "   2. Physical Device (Android/iOS)" -ForegroundColor White
Write-Host "   3. Android Emulator" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

cd Z:\VESIRE_35\Frontend\vesire

switch ($choice) {
    "1" {
        Write-Host "`n🌐 Launching in Chrome..." -ForegroundColor Cyan
        flutter run -d chrome
    }
    "2" {
        Write-Host "`n📱 Launching on physical device..." -ForegroundColor Cyan
        Write-Host "   Make sure your device is connected and USB debugging is enabled" -ForegroundColor Yellow
        flutter run
    }
    "3" {
        Write-Host "`n🤖 Launching Android Emulator..." -ForegroundColor Cyan
        flutter run -d emulator
    }
    default {
        Write-Host "`n🌐 Invalid choice, defaulting to Chrome..." -ForegroundColor Yellow
        flutter run -d chrome
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ AgriScan is now running!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
