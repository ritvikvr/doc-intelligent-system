from ocr_service import extract_text
from chunking_service import create_chunks
from content_quality import is_noise_text
from embeddings_service import generate_embeddings
from vector_store import create_faiss_index, save_index


def process_document(file_path, filename):
    extracted_text = extract_text(file_path)
    if is_noise_text(extracted_text):
        return {
            "status": "skipped",
            "chunks": 0,
            "reason": "Document content could not be extracted into usable text.",
        }

    chunks = create_chunks(extracted_text, filename)
    if not chunks:
        return {
            "status": "skipped",
            "chunks": 0,
            "reason": "No valid chunks were produced from extracted content.",
        }

    texts = [c["text"] for c in chunks]
    embeddings = generate_embeddings(texts)

    index = create_faiss_index(embeddings)
    metadata = chunks

    save_index(index, metadata)

    return {"status": "processed", "chunks": len(chunks)}
