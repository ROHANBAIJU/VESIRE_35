# Run Flutter Script for Windows
# This script sets JAVA_HOME and runs Flutter

$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"
Write-Host "✅ JAVA_HOME set to: $env:JAVA_HOME" -ForegroundColor Green
Write-Host "📱 Running Flutter app..." -ForegroundColor Cyan

# Check if we're in the correct directory
if (Test-Path "pubspec.yaml") {
    flutter run -d windows
} else {
    Write-Host "❌ Error: Not in Flutter project directory!" -ForegroundColor Red
    Write-Host "Please run this script from: Z:\VESIRE_35\Frontend\vesire" -ForegroundColor Yellow
}
