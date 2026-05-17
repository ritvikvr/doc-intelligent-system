import numpy as np
from vector_store import load_index
from embeddings_service import generate_embeddings
from bm25_service import build_bm25, tokenize_text
from reranker_service import rerank

def reciprocal_rank_fusion(list_of_list_of_indices, k=60):
    rf_scores = {}
    for indices in list_of_list_of_indices:
        for rank, idx in enumerate(indices):
            if idx is None or idx < 0:
                continue
            if idx not in rf_scores:
                rf_scores[idx] = 0.0
            rf_scores[idx] += 1.0 / (k + rank + 1)
    return sorted(rf_scores.keys(), key=lambda x: rf_scores[x], reverse=True)

def retrieve(query: str, top_k=5):
    index, metadata = load_index()

    if index is None or not metadata:
        return []

    query_embedding = generate_embeddings([query])
    if query_embedding is None or len(query_embedding) == 0:
        return []

    try:
        distances, indices = index.search(np.array(query_embedding, dtype="float32"), top_k)
        faiss_results = [i for i in indices[0].tolist() if i is not None and i >= 0]
    except Exception as e:
        print(f"FAISS search error: {e}")
        faiss_results = []

    # --- BM25 ---
    bm25 = build_bm25(metadata)
    bm25_results = []
    if bm25 is not None:
        tokenized_query = tokenize_text(query)
        bm25_scores = bm25.get_scores(tokenized_query)
        bm25_results = np.argsort(bm25_scores)[::-1][:top_k].tolist()

    # --- RRF ---
    fused_indices = reciprocal_rank_fusion([faiss_results, bm25_results])
    if not fused_indices:
        return []

    initial_indices = fused_indices[: min(len(fused_indices), top_k * 3)]
    initial_chunks = [metadata[i] for i in initial_indices if 0 <= i < len(metadata)]
    if not initial_chunks:
        return []

    # --- NEW: RE-RANK ---
    reranked_chunks = rerank(query, initial_chunks)

    return reranked_chunks[:top_k]