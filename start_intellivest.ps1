# IntelliVest AI Launcher for PowerShell
Write-Host "🚀 Starting IntelliVest AI..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
& "$PSScriptRoot\venv\Scripts\Activate.ps1"

# Run the launcher
& "$PSScriptRoot\venv\Scripts\python.exe" "$PSScriptRoot\run_app.py" 