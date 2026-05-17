# Quick start script for development (PowerShell)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Document Intelligence System" -ForegroundColor Green
Write-Host "Quick Start Guide" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check Docker
Write-Host "`nStep 1: Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    $composeVersion = docker-compose --version 2>$null
    if (-not $dockerVersion -or -not $composeVersion) {
        throw "Docker not found"
    }
    Write-Host "✓ Docker and Docker Compose found" -ForegroundColor Green
}
catch {
    Write-Host "✗ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Setup environment
Write-Host "`nStep 2: Setting up environment..." -ForegroundColor Yellow
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file" -ForegroundColor Green
}
else {
    Write-Host "✓ .env already exists" -ForegroundColor Green
}

# Build containers
Write-Host "`nStep 3: Building containers..." -ForegroundColor Yellow
docker-compose build

# Start services
Write-Host "`nStep 4: Starting API service..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services
Write-Host "`nWaiting for service to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✓ Application started successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Available endpoints:" -ForegroundColor Cyan
Write-Host "  API:             http://localhost:8000" -ForegroundColor Green
Write-Host "  API Docs:        http://localhost:8000/docs" -ForegroundColor Green
Write-Host "  Health Check:    http://localhost:8000/health" -ForegroundColor Green
Write-Host ""
Write-Host "Services running:" -ForegroundColor Cyan
Write-Host "  - FastAPI:       localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  View logs:       docker-compose logs -f api" -ForegroundColor Green
Write-Host "  Stop services:   docker-compose down" -ForegroundColor Green
Write-Host "  View all logs:   docker-compose logs -f" -ForegroundColor Green
Write-Host ""
