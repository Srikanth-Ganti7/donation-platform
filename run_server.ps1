# PowerShell script to run the donation platform server
Write-Host "Starting Donation Platform API Server..." -ForegroundColor Green
Write-Host ""

# Kill any existing processes on port 8000
try {
    $processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess
    if ($processes) {
        Write-Host "Stopping existing processes on port 8000..." -ForegroundColor Yellow
        $processes | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
        Start-Sleep 1
    }
} catch {
    # Port 8000 not in use, continue
}

# Change to script directory
Set-Location $PSScriptRoot

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\python.exe") {
    # Start the server using relative path
    & ".venv\Scripts\python.exe" main.py
} else {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    Write-Host "Then install requirements: .venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
