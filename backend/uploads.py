import os
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from ocr_service import extract_text

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

    extracted_text = extract_text(str(file_path))

    return {
        "filename": file.filename,
        "text_preview": extracted_text[:500],
    }
