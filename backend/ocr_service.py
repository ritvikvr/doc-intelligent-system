import os
import PyPDF2
from docx import Document

def extract_text(file_path: str) -> str:
    ext = file_path.split(".")[-1].lower()

    if ext in ["png", "jpg", "jpeg"]:
        return extract_image(file_path)

    elif ext == "pdf":
        return extract_pdf(file_path)

    elif ext == "docx":
        return extract_docx(file_path)

    else:
        return "Unsupported file format"


def extract_image(file_path: str) -> str:
    # Image OCR is disabled to run without Tesseract
    return "Image extraction is currently disabled (requires Tesseract)."


def extract_pdf(file_path: str) -> str:
    full_text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- Page {i+1} ---\n{text}"
    except Exception as e:
        full_text = f"Error reading PDF: {str(e)}"
    return full_text


def extract_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])