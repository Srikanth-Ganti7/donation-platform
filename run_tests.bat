@echo off
echo Running API Tests...
echo.

cd /d "C:\ganti.b\Hackathon\GWH"
"C:\ganti.b\Hackathon\GWH\.venv\Scripts\python.exe" test_api.py

echo.
echo Press any key to continue...
pause
