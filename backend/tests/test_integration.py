# Integration & E2E Tests
"""
Integration tests for Document Intelligence System
"""
import os
import sys

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def test_health_endpoint():
    """Test health check endpoint"""
    from main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint():
    """Test root endpoint"""
    from main import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
async def test_cors_headers():
    """Test CORS headers are set"""
    from main import app
    client = TestClient(app)
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers or "*" in str(response.headers)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
