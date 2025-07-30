# IntelliVest AI Application Launcher
Write-Host "🚀 Starting IntelliVest AI Application..." -ForegroundColor Green
Write-Host ""

# Open the frontend HTML file directly in browser
Write-Host "🌐 Opening frontend in browser..." -ForegroundColor Blue
$frontendPath = Join-Path $PSScriptRoot "frontend\index.html"
Start-Process $frontendPath

Write-Host ""
Write-Host "📊 Starting backend API..." -ForegroundColor Blue

# Activate virtual environment and start backend
& "$PSScriptRoot\venv\Scripts\Activate.ps1"
& "$PSScriptRoot\venv\Scripts\python.exe" -m uvicorn api.main:app --host 127.0.0.1 --port 8001 