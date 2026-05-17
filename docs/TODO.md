# TODO - doc-intelligent-system

## Step 1: Verify runtime deps
- [x] Install dependencies from backend/requirements.txt (may still be running)

## Step 2: Fix FastAPI app wiring
- [ ] Fix missing imports / router definition issues in routes.py
- [ ] Make sure upload/query/analysis routers are correctly defined and included

## Step 3: Fix document processing pipeline
- [ ] Ensure tasks.py imports correct module names (embeddings_service vs embedding_service)
- [ ] Ensure Celery worker task runs and writes FAISS index + metadata

## Step 4: Fix retrieval/RAG request flow
- [ ] Ensure /query calls generate_answer with correct parameters
- [ ] Ensure retrieval_service imports/uses vector_store, embeddings, bm25, rerank consistently

## Step 5: Basic smoke test
- [ ] Start API and hit /health
- [ ] Run upload and then /summary and /entities (or verify gracefully if no index)
