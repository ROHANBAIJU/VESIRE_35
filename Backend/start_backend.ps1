# AgriScan Quick Start Script
# This script starts the backend server

Write-Host "🚀 Starting AgriScan Backend Server..." -ForegroundColor Green
Write-Host ""

# Navigate to backend directory
$BackendPath = "z:\VESIRE_35\Backend"
Set-Location $BackendPath

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Cyan
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️ Virtual environment not found. Using system Python..." -ForegroundColor Yellow
}

# Check if requirements are installed
Write-Host "📋 Checking dependencies..." -ForegroundColor Cyan
python -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Flask not found! Installing dependencies..." -ForegroundColor Red
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "✅ Starting Flask API Server..." -ForegroundColor Green
Write-Host "📡 Server will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📡 For Android Emulator use: http://10.0.2.2:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔍 Find your IP for physical device:" -ForegroundColor Yellow
Write-Host "   Windows: ipconfig" -ForegroundColor Gray
Write-Host "   Then use: http://YOUR_IP:5000" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Start the Flask server
python -m api.app
