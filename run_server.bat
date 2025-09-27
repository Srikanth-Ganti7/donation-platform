@echo off
echo Starting Donation Platform API Server...
echo.
echo Checking for available ports...
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Kill any existing processes on port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 2^>nul') do (
    echo Stopping existing process on port 8000...
    taskkill /F /PID %%a >nul 2>&1
)

REM Use relative path to Python executable
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then install requirements: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Server stopped. Press any key to exit...
pause
