# scripts/dev.ps1
$ErrorActionPreference = "Stop"

Write-Host "Starting database..."
docker compose up -d

# Activate venv (Windows venv path is different)
.\.venv\Scripts\Activate.ps1

Write-Host "Starting backend..."
Set-Location backend


# Start backend in a new PowerShell process
$backendProcess = Start-Process powershell `
  -ArgumentList "uvicorn app.main:app --reload" `
  -PassThru

Write-Host "Starting frontend..."
Set-Location ..\desktop
npm run tauri dev

# When frontend exits, stop backend
Write-Host "Stopping backend..."
Stop-Process -Id $backendProcess.Id
