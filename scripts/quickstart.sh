#!/bin/bash
# Quick start script for development

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo "Document Intelligence System"
echo "Quick Start Guide"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Checking Docker${NC}"
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Desktop first."
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"

echo -e "\n${YELLOW}Step 2: Setting up environment${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
else
    echo -e "${GREEN}✓ .env already exists${NC}"
fi

echo -e "\n${YELLOW}Step 3: Building containers${NC}"
docker-compose build

echo -e "\n${YELLOW}Step 4: Starting API service${NC}"
docker-compose up -d

echo -e "\n${GREEN}=========================================="
echo "✓ Application started successfully!"
echo "==========================================${NC}"
echo ""
echo -e "Available endpoints:"
echo -e "  API:             ${GREEN}http://localhost:8000${NC}"
echo -e "  API Docs:        ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  Health Check:    ${GREEN}http://localhost:8000/health${NC}"
echo ""
echo -e "Services running:"
echo -e "  - FastAPI:       ${GREEN}localhost:8000${NC}"
echo ""
echo -e "Useful commands:"
echo -e "  View logs:       ${GREEN}docker-compose logs -f api${NC}"
echo -e "  Stop services:   ${GREEN}docker-compose down${NC}"
echo -e "  View all logs:   ${GREEN}docker-compose logs -f${NC}"
echo ""
