"""
Exercise: RAG API
Chapter 11: Retrieval-Augmented Generation (RAG)

Goal: Wrap the RAG pipeline behind a FastAPI application with a POST /ask endpoint
that accepts a question and returns an answer with source citations.

Skills practiced:
- Serving a RAG pipeline as an HTTP API with FastAPI
- Lifespan events for one-time index setup at startup
- Pydantic request/response models
- Connecting the retrieve + generate steps inside an async route handler

Instructions:
1. Implement the startup lifespan function to load, chunk, embed, and index the
   knowledge base once when the server starts. Store the index and chunks in the
   app state so the route handler can access them.
2. Implement the /ask route handler: call retrieve(), build_rag_prompt(), and
   get_completion() to produce a cited answer.
3. Start the server with the uvicorn command in the comment below.
4. Test with: curl -X POST http://localhost:8000/ask -H "Content-Type: application/json"
              -d '{"question": "How do I cancel my subscription?"}'

Run (server):
    uvicorn solutions.ch11.rag_api:app --reload  (from the repo root)

Or directly:
    python solutions/ch11/rag_api.py  (from the repo root)
"""

import os
import sys
from contextlib import asynccontextmanager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
import litellm  # noqa: E402 - used directly for embedding calls
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from shared import get_completion

# NOTE: embedding model name may need adjusting per provider.
# OpenAI: "text-embedding-3-small" | Google: "gemini/text-embedding-004"
EMBEDDING_MODEL = "text-embedding-3-small"

try:
    import faiss
except ImportError:
    print("faiss-cpu is required. Run: pip install faiss-cpu")
    sys.exit(1)

KB_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "exercises", "ch11", "knowledge-base")
)
CHUNK_SIZE = 500
OVERLAP = 50
TOP_K = 3

RAG_SYSTEM = (
    "Answer the user's question based ONLY on the provided context.\n"
    "If the context does not contain the answer, say "
    "'I don't have enough information to answer that.'\n"
    "Always cite your sources using [Source: filename]."
)

# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------


def _load_and_index(docs_dir):
    """Load docs from docs_dir, chunk, embed, and return (faiss_index, chunks)."""
    # Load
    documents = []
    for fname in sorted(os.listdir(docs_dir)):
        if fname.endswith(".md"):
            fpath = os.path.join(docs_dir, fname)
            with open(fpath, "r") as f:
                documents.append({"filename": fname, "content": f.read()})

    # Chunk
    chunks = []
    step = CHUNK_SIZE - OVERLAP
    for doc in documents:
        text = doc["content"]
        start, chunk_num = 0, 0
        while start < len(text):
            chunks.append({
                "text": text[start:start + CHUNK_SIZE],
                "source": doc["filename"],
                "chunk_id": chunk_num,
            })
            start += step
            chunk_num += 1

    # Embed
    texts = [c["text"] for c in chunks]
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=texts)
    vectors = np.array(
        [item["embedding"] for item in resp["data"]],
        dtype=np.float32,
    )

    # Index
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    return index, chunks


def _retrieve(query, index, chunks, k=TOP_K):
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=[query])
    q_vec = np.array([resp["data"][0]["embedding"]], dtype=np.float32)
    distances, indices = index.search(q_vec, k)
    return [chunks[i] for i in indices[0]]


def _build_rag_prompt(query, retrieved_chunks):
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in retrieved_chunks
    )
    return [
        {"role": "system", "content": RAG_SYSTEM},
        {"role": "user", "content": f"Context:\n{context}\n\n---\n\nQuestion: {query}"},
    ]


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


# ---------------------------------------------------------------------------
# FastAPI app with lifespan for one-time index build
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the RAG index once at startup; clean up on shutdown."""
    print(f"Building RAG index from {KB_DIR}...")
    app.state.index, app.state.chunks = _load_and_index(KB_DIR)
    print(f"  Index ready: {app.state.index.ntotal} vectors")
    yield
    # Shutdown: nothing to clean up for an in-memory FAISS index


app = FastAPI(title="RAG API", version="1.0.0", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Route handler
# ---------------------------------------------------------------------------


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """Retrieve relevant chunks and generate a cited answer.

    Request body: {"question": "your question here"}
    Response:     {"answer": "...", "sources": ["file.md", ...]}
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="question must not be empty")

    retrieved = _retrieve(request.question, app.state.index, app.state.chunks)
    messages = _build_rag_prompt(request.question, retrieved)
    answer = get_completion(messages, temperature=0.0)
    sources = list(dict.fromkeys(c["source"] for c in retrieved))
    return AskResponse(answer=answer, sources=sources)


# ---------------------------------------------------------------------------
# Dev runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("solutions.ch11.rag_api:app", host="0.0.0.0", port=8000, reload=True)


# Expected interaction (illustrative):
# $ uvicorn solutions.ch11.rag_api:app --reload
# INFO:     Building RAG index from .../knowledge-base...
# INFO:     Index ready: 11 vectors
# INFO:     Uvicorn running on http://0.0.0.0:8000
#
# $ curl -s -X POST http://localhost:8000/ask \
#        -H "Content-Type: application/json" \
#        -d '{"question": "How do I cancel my subscription?"}' | python3 -m json.tool
# {
#     "answer": "Go to Settings > Billing > Subscription and click Cancel Plan.
#                Cancellation takes effect at the end of the current billing
#                period. [Source: billing-faq.md]",
#     "sources": ["billing-faq.md"]
# }
