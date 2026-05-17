import uuid
import re

def split_into_pages(raw_text: str):
    pages = re.split(r"--- Page \d+ ---", raw_text)
    return [p.strip() for p in pages if p.strip()]


def chunk_text(text: str, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


def create_chunks(raw_text: str, filename: str):
    pages = split_into_pages(raw_text)
    all_chunks = []

    for page_num, page_text in enumerate(pages, start=1):
        chunks = chunk_text(page_text)

        for chunk in chunks:
            all_chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "text": chunk,
                "page": page_num,
                "source": filename
            })

    return all_chunks