@echo off
echo Starting IntelliVest AI Application...
echo.
echo Opening frontend in browser...
start "" "frontend\index.html"
echo.
echo Starting backend API...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m uvicorn api.main:app --host 127.0.0.1 --port 8001
pause 