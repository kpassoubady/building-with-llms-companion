"""
Exercise: RAG Pipeline
Chapter 11: Retrieval-Augmented Generation (RAG)

Goal: Build a complete end-to-end RAG pipeline that ingests Markdown files from
a knowledge base, chunks and embeds them, builds a FAISS index, retrieves the
top-k chunks for a query, and generates a cited answer.

Skills practiced:
- Ingestion pipeline: load -> chunk -> embed -> store
- Query pipeline: embed query -> FAISS search -> augment prompt -> generate
- Attaching source metadata to chunks for citation
- Grounding the LLM with "Answer ONLY from the provided context"

Instructions:
1. Implement load_documents() to read all .md files from the knowledge base directory.
2. Implement chunk_documents() to split each document and attach source + chunk_id.
3. Implement embed_chunks() to embed all chunk texts in a single litellm call.
4. Implement build_index() to create a FAISS IndexFlatL2 from the embeddings.
5. Implement retrieve() to embed the query and search the index for top-k chunks.
6. Implement build_rag_prompt() to format retrieved context with source labels.
7. Run main() and check that the answers reference the correct source files.

Run: python solutions/ch11/rag_pipeline.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
import litellm  # noqa: E402 - used directly for embedding calls
from shared import get_completion

# NOTE: embedding model name may need adjusting per provider.
# OpenAI: "text-embedding-3-small" | Google: "gemini/text-embedding-004"
EMBEDDING_MODEL = "text-embedding-3-small"

try:
    import faiss
except ImportError:
    print("faiss-cpu is required. Run: pip install faiss-cpu")
    sys.exit(1)

# Path to the sample knowledge base shipped with this exercise
KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "exercises", "ch11", "knowledge-base")
KB_DIR = os.path.normpath(KB_DIR)

CHUNK_SIZE = 500
OVERLAP = 50
TOP_K = 3

SAMPLE_QUERIES = [
    "What happens if a payment fails?",
    "What training must new employees complete in the first 30 days?",
    "How do I cancel my subscription?",
]

RAG_SYSTEM = (
    "Answer the user's question based ONLY on the provided context.\n"
    "If the context does not contain the answer, say "
    "'I don't have enough information to answer that.'\n"
    "Always cite your sources using [Source: filename]."
)

# ---------------------------------------------------------------------------
# Ingestion pipeline
# ---------------------------------------------------------------------------


def load_documents(docs_dir):
    """Read all .md files from docs_dir and return a list of document dicts.

    Args:
        docs_dir: Path to the directory containing .md files.

    Returns:
        List of dicts with keys: filename, content.
    """
    documents = []
    for fname in sorted(os.listdir(docs_dir)):
        if fname.endswith(".md"):
            fpath = os.path.join(docs_dir, fname)
            with open(fpath, "r") as f:
                documents.append({"filename": fname, "content": f.read()})
    return documents


def chunk_documents(documents, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split each document into overlapping character chunks and attach metadata.

    Args:
        documents: List of dicts from load_documents().
        chunk_size: Maximum characters per chunk.
        overlap: Characters of shared context between consecutive chunks.

    Returns:
        List of chunk dicts with keys: text, source, chunk_id.
    """
    chunks = []
    for doc in documents:
        text = doc["content"]
        start, chunk_num = 0, 0
        step = chunk_size - overlap
        while start < len(text):
            chunks.append({
                "text": text[start:start + chunk_size],
                "source": doc["filename"],
                "chunk_id": chunk_num,
            })
            start += step
            chunk_num += 1
    return chunks


def embed_chunks(chunks):
    """Embed the text of every chunk in a single litellm call.

    Args:
        chunks: List of chunk dicts (must have a "text" key).

    Returns:
        numpy array of shape (N, D), dtype float32.
    """
    texts = [c["text"] for c in chunks]
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=texts)
    vectors = [item["embedding"] for item in resp["data"]]
    return np.array(vectors, dtype=np.float32)


def build_index(vectors):
    """Create and populate a FAISS IndexFlatL2 from a numpy array of vectors.

    Args:
        vectors: numpy array of shape (N, D), dtype float32.

    Returns:
        faiss.IndexFlatL2 containing all N vectors.
    """
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index


# ---------------------------------------------------------------------------
# Query pipeline
# ---------------------------------------------------------------------------


def retrieve(query, index, chunks, k=TOP_K):
    """Embed the query, search the FAISS index, and return top-k chunk dicts.

    Args:
        query: User question string.
        index: FAISS index (output of build_index).
        chunks: Parallel metadata list (same order as index vectors).
        k: Number of chunks to retrieve.

    Returns:
        List of chunk dicts (text, source, chunk_id) for the top-k matches.
    """
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=[query])
    q_vec = np.array([resp["data"][0]["embedding"]], dtype=np.float32)
    distances, indices = index.search(q_vec, k)
    return [chunks[i] for i in indices[0]]


def build_rag_prompt(query, retrieved_chunks):
    """Format the retrieved context into a prompt ready for get_completion.

    Args:
        query: User question string.
        retrieved_chunks: List of chunk dicts from retrieve().

    Returns:
        List of message dicts: [{"role": "system", ...}, {"role": "user", ...}]
    """
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in retrieved_chunks
    )
    return [
        {"role": "system", "content": RAG_SYSTEM},
        {"role": "user", "content": f"Context:\n{context}\n\n---\n\nQuestion: {query}"},
    ]


def rag_query(query, index, chunks):
    """Run the full query pipeline for a single question.

    Args:
        query: User question string.
        index: FAISS index.
        chunks: Parallel metadata list.

    Returns:
        Dict with keys: answer (str), sources (list of unique source filenames).
    """
    retrieved = retrieve(query, index, chunks)
    messages = build_rag_prompt(query, retrieved)
    answer = get_completion(messages, temperature=0.0)
    sources = list(dict.fromkeys(c["source"] for c in retrieved))
    return {"answer": answer, "sources": sources}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 11 - RAG Pipeline\n")

    print(f"Loading documents from {KB_DIR}...")
    docs = load_documents(KB_DIR)
    print(f"  Loaded {len(docs)} documents: {[d['filename'] for d in docs]}")

    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"  Created {len(chunks)} chunks")

    print("Embedding chunks...")
    vectors = embed_chunks(chunks)
    print(f"  Vectors shape: {vectors.shape}")

    print("Building FAISS index...")
    index = build_index(vectors)
    print(f"  Index ready: {index.ntotal} vectors\n")

    for query in SAMPLE_QUERIES:
        print(f"Q: {query}")
        result = rag_query(query, index, chunks)
        print(f"A: {result['answer'].strip()}")
        print(f"   Sources: {result['sources']}")
        print()


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# Chapter 11 - RAG Pipeline
#
# Loading documents from .../knowledge-base...
#   Loaded 2 documents: ['billing-faq.md', 'onboarding.md']
# Chunking documents...
#   Created 11 chunks
# Embedding chunks...
#   Vectors shape: (11, 1536)
# Building FAISS index...
#   Index ready: 11 vectors
#
# Q: What happens if a payment fails?
# A: If a payment fails, it is retried automatically on days 3, 7, and 14.
#    After day 14 the account is suspended. [Source: billing-faq.md]
#    Sources: ['billing-faq.md']
#
# Q: What training must new employees complete in the first 30 days?
# A: New employees must complete security awareness, code of conduct, and
#    data privacy training within 30 days. [Source: onboarding.md]
#    Sources: ['onboarding.md']
