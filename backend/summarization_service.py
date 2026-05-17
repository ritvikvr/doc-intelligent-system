from content_quality import is_noise_text, top_sentences_for_summary
from response_style import format_client_ready_summary
from vector_store import load_index


def summarize_document():
    index, metadata = load_index()
    if not metadata:
        return "No document found."

    valid_chunks = [
        c for c in metadata
        if (c.get("text") or "").strip() and not is_noise_text(c.get("text", ""))
    ]
    if not valid_chunks:
        return "No high-quality document content is available for summarization."

    texts = [c.get("text", "") for c in valid_chunks]
    top_sentences = top_sentences_for_summary(texts, max_sentences=8)
    if not top_sentences:
        return "No summary available for the indexed document."

    sources = sorted({c.get("source", "unknown") for c in valid_chunks})
    page_count = len({c.get("page") for c in valid_chunks if c.get("page") is not None})

    exec_points = top_sentences[:3]
    detail_points = top_sentences[3:8]

    return format_client_ready_summary(
        processed_sources=len(sources),
        extracted_pages=page_count,
        executive_points=exec_points,
        findings=detail_points or exec_points[:2],
    )
