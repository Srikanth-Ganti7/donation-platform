@echo off
echo ========================================
echo  Donation Platform - First Time Setup
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo 1. Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or later from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python --version
echo ✓ Python is installed
echo.

echo 2. Creating virtual environment...
if exist ".venv" (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv .venv
    echo ✓ Virtual environment created
)
echo.

echo 3. Installing dependencies...
.venv\Scripts\pip install -r requirements.txt
echo ✓ Dependencies installed
echo.

echo 4. Verifying installation...
.venv\Scripts\python -c "import fastapi; print('✓ FastAPI installed correctly')"
echo.

echo ========================================
echo  Setup Complete! 
echo ========================================
echo.
echo You can now run the server using:
echo   .\run_server.bat
echo.
echo Or activate the environment manually:
echo   .\activate_env.bat
echo.
pause
