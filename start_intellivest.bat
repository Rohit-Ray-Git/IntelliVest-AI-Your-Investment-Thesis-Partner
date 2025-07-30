@echo off
echo Starting IntelliVest AI...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the launcher
python run_app.py

pause 