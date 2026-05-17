# Document Intelligence System - Startup Script (PowerShell)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Document Intelligence System Startup" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

if (!(Test-Path .env)) {
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -q -r backend/requirements.txt

Write-Host ""
Write-Host "Running application tests..." -ForegroundColor Yellow
python backend/tests/test_app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed! Please fix the errors above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Creating required directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path uploads | Out-Null
New-Item -ItemType Directory -Force -Path data/embeddings | Out-Null
New-Item -ItemType Directory -Force -Path data/raw | Out-Null

Write-Host ""
Write-Host "Starting application with Docker Compose..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Application started!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "API available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "To view logs: docker-compose logs -f api" -ForegroundColor Cyan
Write-Host "To stop: docker-compose down" -ForegroundColor Cyan
