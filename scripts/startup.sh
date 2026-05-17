#!/bin/bash

# Document Intelligence System - Startup Script

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo "Document Intelligence System Startup"
echo "=========================================="

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

echo "Installing Python dependencies..."
pip install -q -r backend/requirements.txt

echo ""
echo "Running application tests..."
python backend/tests/test_app.py

echo ""
echo "Creating required directories..."
mkdir -p uploads data/embeddings data/raw

echo ""
echo "Starting application with Docker Compose..."
docker-compose up -d

echo ""
echo "=========================================="
echo "Application started!"
echo "=========================================="
echo "API available at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo "Health check: http://localhost:8000/health"
echo ""
echo "To view logs: docker-compose logs -f api"
echo "To stop: docker-compose down"
