@echo off
echo ========================================
echo  Donation Platform - Run All Tests
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Checking if server is running...
curl -s http://localhost:8000/ping >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  SERVER NOT RUNNING!
    echo.
    echo Please start the server first:
    echo   .\run_server.bat
    echo.
    echo Then run this test script again.
    pause
    exit /b 1
)

echo ✅ Server is running!
echo.

echo Running comprehensive automated tests...
echo.

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" comprehensive_test.py
) else (
    python comprehensive_test.py
)

echo.
echo ========================================
echo For manual testing, see MANUAL_TESTING.md
echo Or visit: http://localhost:8000/docs
echo ========================================
echo.
pause
