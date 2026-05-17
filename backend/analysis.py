from fastapi import APIRouter
from summarization_service import summarize_document

router = APIRouter()


@router.get("/summary")
def get_summary():
    return {"summary": summarize_document()}
