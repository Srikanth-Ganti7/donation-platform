# PowerShell script to run the donation platform server
Write-Host "Starting Donation Platform API Server..." -ForegroundColor Green
Write-Host ""
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Interactive docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Alternative docs: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\ganti.b\Hackathon\GWH"

# Start the server
& "C:\ganti.b\Hackathon\GWH\.venv\Scripts\python.exe" main.py
