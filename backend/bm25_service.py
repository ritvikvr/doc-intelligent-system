import re
from rank_bm25 import BM25Okapi


def tokenize_text(text):
    return re.findall(r"\w+", text.lower())


def build_bm25(metadata):
    corpus = [tokenize_text(chunk.get("text", "")) for chunk in metadata if chunk.get("text")]
    if not corpus:
        return None
    return BM25Okapi(corpus)