@echo off
echo ========================================
echo  Donation Platform - Phase 2 Setup
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo 1. Running database migration for Phase 2...
.venv\Scripts\python.exe migrate_database.py
echo.

echo 2. Starting server to test Phase 2 features...
echo Press Ctrl+C to stop the server when done testing
echo.
.venv\Scripts\python.exe main.py
