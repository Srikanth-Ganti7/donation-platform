@echo off
echo Activating virtual environment...
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo.
    echo Virtual environment activated!
    echo You can now run: python main.py
    echo.
    cmd /k
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then install requirements: .venv\Scripts\pip install -r requirements.txt
    pause
)
