import hashlib
import re

import numpy as np

EMBED_DIM = 256
TOKEN_RE = re.compile(r"\w+")


def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall((text or "").lower())


def _embed_text(text: str) -> np.ndarray:
    vec = np.zeros(EMBED_DIM, dtype=np.float32)
    tokens = _tokenize(text)
    if not tokens:
        return vec

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:2], "big") % EMBED_DIM
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vec[idx] += sign

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


def generate_embeddings(texts):
    return np.array([_embed_text(t) for t in texts], dtype=np.float32)
