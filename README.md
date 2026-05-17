# doc-intelligent-system

Document Intelligence System using FastAPI only (synchronous processing, no PostgreSQL/Redis/Celery).

## Restructured Layout

- `frontend/` static UI (`index.html`)
- `backend/` API, services, dependencies, and tests
- `scripts/` startup and quickstart scripts
- `docs/` documentation and planning notes

## Quick Start

### macOS/Linux
```bash
bash scripts/quickstart.sh
```

### Windows (PowerShell)
```powershell
./scripts/quickstart.ps1
```

## Run Tests

```bash
python backend/tests/test_app.py
```

## Detailed Docs

- `docs/TESTING_GUIDE.md`
- `docs/TODO.md`
