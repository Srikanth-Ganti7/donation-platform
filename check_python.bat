@echo off
echo Verifying Python Environment Setup...
echo.

echo Testing system Python:
python -c "import sys; print('System Python:', sys.executable)"
echo.

echo Testing virtual environment Python:
"C:\ganti.b\Hackathon\GWH\.venv\Scripts\python.exe" -c "import sys; print('Virtual Env Python:', sys.executable)"
echo.

echo Testing FastAPI import in virtual environment:
"C:\ganti.b\Hackathon\GWH\.venv\Scripts\python.exe" -c "import fastapi; print('✓ FastAPI available in virtual environment')"
echo.

echo Testing FastAPI import in system Python:
python -c "try: import fastapi; print('✓ FastAPI available in system Python'); except ImportError: print('✗ FastAPI NOT available in system Python')"
echo.

echo ============================================
echo SOLUTION: Use one of these methods to run your server:
echo.
echo 1. Use batch file:    .\run_server.bat
echo 2. Activate venv:     .\.venv\Scripts\activate.bat
echo 3. Use full path:     "C:\ganti.b\Hackathon\GWH\.venv\Scripts\python.exe" main.py
echo.
pause
