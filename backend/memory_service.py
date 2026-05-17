import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = PROJECT_ROOT / "data" / "sessions"


def _session_file(session_id: str) -> Path:
    safe_id = "".join(c for c in session_id if c.isalnum() or c in ("-", "_"))
    if not safe_id:
        safe_id = "default"
    return SESSIONS_DIR / f"{safe_id}.jsonl"


def save_message(session_id, role, content):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    message = {"role": role, "content": content}
    with _session_file(session_id).open("a", encoding="utf-8") as f:
        f.write(json.dumps(message) + "\n")


def get_history(session_id):
    path = _session_file(session_id)
    if not path.exists():
        return []

    history = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
            if isinstance(message, dict) and "role" in message and "content" in message:
                history.append(message)
        except json.JSONDecodeError:
            continue
    return history
