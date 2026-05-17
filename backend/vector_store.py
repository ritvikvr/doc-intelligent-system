import os
import pickle
from pathlib import Path

import faiss
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"
INDEX_PATH = EMBEDDINGS_DIR / "faiss.index"
META_PATH = EMBEDDINGS_DIR / "metadata.pkl"


def create_faiss_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index


def save_index(index, metadata):
    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)


def load_index():
    if not INDEX_PATH.exists():
        return None, None

    index = faiss.read_index(str(INDEX_PATH))

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
