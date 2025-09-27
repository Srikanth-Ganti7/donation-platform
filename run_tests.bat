@echo off
echo Running API Tests...
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if virtual environment and test file exist
if exist ".venv\Scripts\python.exe" (
    if exist "test_api.py" (
        ".venv\Scripts\python.exe" test_api.py
    ) else (
        echo ERROR: test_api.py not found!
        echo Make sure you're running this from the project directory.
    )
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then install requirements: .venv\Scripts\pip install -r requirements.txt
)

echo.
echo Press any key to continue...
pause
