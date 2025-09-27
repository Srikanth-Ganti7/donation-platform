@echo off
echo Starting Donation Platform API Server...
echo.
echo Server will be available at: http://localhost:8000
echo Interactive docs: http://localhost:8000/docs
echo Alternative docs: http://localhost:8000/redoc
echo.

cd /d "C:\ganti.b\Hackathon\GWH"
"C:\ganti.b\Hackathon\GWH\.venv\Scripts\python.exe" main.py

echo.
echo Server stopped. Press any key to exit...
pause
