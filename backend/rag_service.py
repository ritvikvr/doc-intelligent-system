import os

import requests

from content_quality import is_noise_text, top_sentences_for_question
from memory_service import get_history, save_message
from response_style import extract_points_from_groq_response, format_client_ready_answer
from retrieval_service import retrieve

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1")


def call_groq(prompt: str, max_output_tokens: int = 250) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    base = GROQ_API_URL.rstrip("/")
    url = f"{base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an enterprise knowledge assistant for a professional IT services company. "
                    "Use only provided context. Keep language precise, factual, and concise. "
                    "Return output strictly with sections in this order: "
                    "Client-Ready Response, Executive Summary, Key Findings, Business Impact, "
                    "Risks and Dependencies, Recommended Next Steps. "
                    "Use bullet points under each section. If information is missing, state it explicitly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": max_output_tokens,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    choices = data.get("choices") or []
    if not choices:
        return ""
    return (choices[0].get("message") or {}).get("content", "") or ""


def _local_answer(question: str, chunks: list[dict]) -> str:
    valid_chunks = [
        c for c in chunks
        if (c.get("text") or "").strip() and not is_noise_text(c.get("text", ""))
    ]
    if not valid_chunks:
        return format_client_ready_answer(
            executive_points=[],
            findings=[],
            include_unknown_notice=True,
        )

    sentences = top_sentences_for_question(
        question=question,
        texts=[c.get("text", "") for c in valid_chunks],
        max_sentences=5,
    )
    if not sentences:
        return format_client_ready_answer(
            executive_points=[],
            findings=[],
            include_unknown_notice=True,
        )

    executive = sentences[:2]
    findings = sentences[2:5]
    return format_client_ready_answer(executive_points=executive, findings=findings or executive)


def generate_answer(question: str, session_id: str, use_groq: bool = False):
    _ = get_history(session_id)
    chunks = retrieve(question)
    chunks = [c for c in chunks if not is_noise_text(c.get("text", ""))]

    if use_groq:
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not configured for Groq-based generation.")
        context = "\n\n".join([c.get("text", "") for c in chunks[:6] if c.get("text")])
        prompt = (
            "Answer this as a concise client-ready IT advisory note for leadership.\n"
            "Use only the context below. If unknown, state that clearly.\n\n"
            f"Context:\n{context or 'No relevant document context was found.'}\n\n"
            f"Question:\n{question}"
        )
        raw_answer = call_groq(prompt, max_output_tokens=420)
        points = extract_points_from_groq_response(raw_answer, max_points=6)
        if points:
            answer = format_client_ready_answer(
                executive_points=points[:2],
                findings=points[2:6] or points[:2],
            )
        else:
            answer = format_client_ready_answer(
                executive_points=[],
                findings=[],
                include_unknown_notice=True,
            )
    else:
        answer = _local_answer(question, chunks)

    save_message(session_id, "user", question)
    save_message(session_id, "assistant", answer)

    citations = list({f"Page {c.get('page', 'Unknown')}" for c in chunks if c.get('page') is not None})
    if not citations:
        citations = ["Page Unknown"]

    return {
        "answer": answer,
        "citations": citations,
    }
