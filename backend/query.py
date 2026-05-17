from datetime import datetime
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rag_service import generate_answer

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "data" / "question_logs.jsonl"


class QueryRequest(BaseModel):
    question: str
    session_id: str
    use_groq: bool = False


def save_question_log(username: str, question: str, session_id: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username,
        "session_id": session_id,
        "question": question,
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")


@router.post("/query")
def query_docs(
    request: QueryRequest,
):
    try:
        result = generate_answer(request.question, request.session_id, use_groq=request.use_groq)
        save_question_log("guest", request.question, request.session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/query/groq")
def query_groq(
    request: QueryRequest,
):
    try:
        result = generate_answer(request.question, request.session_id, use_groq=True)
        save_question_log("guest", request.question, request.session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
