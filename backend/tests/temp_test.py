import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import app

client = TestClient(app)
print("health", client.get("/health").status_code, client.get("/health").json())

register_payload = {"username": "temp_user", "password": "temp_password"}
client.post("/auth/register", json=register_payload)
login_resp = client.post("/auth/login", json=register_payload)
token = login_resp.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"} if token else {}

path = PROJECT_ROOT / "data" / "raw" / "test.txt"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(b"test file content")

with path.open("rb") as f:
    r = client.post("/upload", files={"file": ("test.txt", f, "text/plain")})
print("/upload", r.status_code, r.text)

r = client.post("/query", json={"question": "hello", "session_id": "test"}, headers=headers)
print("/query", r.status_code, r.text)
