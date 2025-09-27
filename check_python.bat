@echo off
echo Verifying Python Environment Setup...
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Testing system Python:
python -c "import sys; print('System Python:', sys.executable)" 2>nul
if errorlevel 1 (
    echo System Python not found or not working
)
echo.

echo Testing virtual environment Python:
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; print('Virtual Env Python:', sys.executable)"
) else (
    echo Virtual environment not found!
)
echo.

echo Testing FastAPI import in virtual environment:
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "try: import fastapi; print('✓ FastAPI available in virtual environment')" 2>nul || echo "✗ FastAPI NOT available in virtual environment"
) else (
    echo Cannot test - virtual environment not found
)
echo.

echo Testing FastAPI import in system Python:
python -c "try: import fastapi; print('✓ FastAPI available in system Python'); except ImportError: print('✗ FastAPI NOT available in system Python')" 2>nul
echo.

echo ============================================
echo SOLUTION: Use one of these methods to run your server:
echo.
echo 1. Use batch file:    .\run_server.bat
echo 2. Activate venv:     .\activate_env.bat
echo 3. Use relative path: .\.venv\Scripts\python.exe main.py
echo.
pause
