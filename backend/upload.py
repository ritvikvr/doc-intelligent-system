import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from tasks import process_document

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = PROJECT_ROOT / "data" / "raw"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    document_id = str(uuid4())

    try:
        result = process_document(str(file_path), file.filename)
        return {
            "message": "File uploaded and processed successfully.",
            "document_id": document_id,
            "filename": file.filename,
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
