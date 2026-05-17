import re
from collections import Counter

NOISE_PATTERNS = (
    "unsupported file format",
    "image extraction is currently disabled",
    "error reading pdf",
    "no document found",
)

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "have", "in", "is", "it", "its", "of", "on", "or", "that",
    "the", "to", "was", "were", "will", "with", "this", "these", "those",
    "their", "there", "than", "then", "but", "if", "into", "about",
}

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[a-zA-Z0-9]{3,}")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def is_noise_text(text: str) -> bool:
    cleaned = normalize_text(text).lower()
    if not cleaned:
        return True
    return any(pattern in cleaned for pattern in NOISE_PATTERNS)


def tokenize(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def split_sentences(text: str) -> list[str]:
    parts = SENTENCE_RE.split(normalize_text(text))
    return [p.strip() for p in parts if len(p.strip().split()) >= 6]


def _base_word_scores(sentences: list[str]) -> Counter:
    counts: Counter = Counter()
    for s in sentences:
        for token in tokenize(s):
            if token not in STOP_WORDS:
                counts[token] += 1
    return counts


def top_sentences_for_summary(texts: list[str], max_sentences: int = 8) -> list[str]:
    sentences = []
    for text in texts:
        sentences.extend(split_sentences(text))
    if not sentences:
        return []

    word_scores = _base_word_scores(sentences)
    ranked = []
    for s in sentences:
        tokens = [t for t in tokenize(s) if t not in STOP_WORDS]
        score = sum(word_scores.get(t, 0) for t in tokens)
        ranked.append((score, s))

    ranked.sort(key=lambda x: x[0], reverse=True)
    selected = []
    seen = set()
    for _, sentence in ranked:
        key = sentence.lower()
        if key in seen:
            continue
        seen.add(key)
        selected.append(sentence)
        if len(selected) >= max_sentences:
            break
    return selected


def top_sentences_for_question(
    question: str,
    texts: list[str],
    max_sentences: int = 5,
) -> list[str]:
    sentences = []
    for text in texts:
        sentences.extend(split_sentences(text))
    if not sentences:
        return []

    q_tokens = {t for t in tokenize(question) if t not in STOP_WORDS}
    word_scores = _base_word_scores(sentences)
    ranked = []
    for s in sentences:
        s_tokens = [t for t in tokenize(s) if t not in STOP_WORDS]
        overlap = len(q_tokens.intersection(s_tokens))
        density = sum(word_scores.get(t, 0) for t in s_tokens)
        score = (overlap * 10) + density
        ranked.append((score, s))

    ranked.sort(key=lambda x: x[0], reverse=True)
    selected = []
    seen = set()
    for _, sentence in ranked:
        key = sentence.lower()
        if key in seen:
            continue
        seen.add(key)
        selected.append(sentence)
        if len(selected) >= max_sentences:
            break
    return selected

