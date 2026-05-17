import re

TOKEN_RE = re.compile(r"\w+")


def _tokenize(text: str) -> set[str]:
    return set(TOKEN_RE.findall((text or "").lower()))


def _score(query: str, text: str) -> float:
    q = _tokenize(query)
    t = _tokenize(text)
    if not q or not t:
        return 0.0
    overlap = len(q & t)
    return overlap / max(1, len(q))


def rerank(query, chunks):
    if not chunks:
        return []

    for chunk in chunks:
        chunk["score"] = float(_score(query, chunk.get("text", "")))

    return sorted(chunks, key=lambda x: x.get("score", 0.0), reverse=True)
