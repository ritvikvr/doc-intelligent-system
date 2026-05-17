# Document Intelligence System - Testing and Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local testing)
- Tesseract OCR installed (for local testing)

## Local Testing

### 1. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Run Application Tests
```bash
python backend/tests/test_app.py
```

## Docker Deployment

### 1. Build and Start API
```bash
# Windows (PowerShell)
./scripts/startup.ps1

# macOS/Linux
bash scripts/startup.sh
```

### 2. Manual Docker Commands
```bash
docker build -t doc-intelligent-system .
docker-compose up -d
docker-compose logs -f api
docker-compose down
docker-compose down -v
```

## Restructured Folders

- `frontend/index.html` serves the root page (`GET /`)
- `backend/` contains API modules and processing logic
- `backend/tests/` contains smoke and integration tests
- `data/` stores runtime embeddings, uploads, auth users, question logs, and chat sessions

## Endpoints

- `GET /health` - Health check
- `GET /` - Root endpoint, serves `frontend/index.html`
- `POST /upload` - Upload and process document synchronously
- `POST /query` - Query documents

## Troubleshooting

### API Not Starting
```bash
docker-compose logs -f api
```
