import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

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
KB_DIR = os.path.join(os.path.dirname(__file__), "knowledge-base")

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
    # TODO: Use os.listdir() to find files ending with ".md".
    #   Open each, read the content, and append {"filename": name, "content": text}.
    #   Sort by filename so ingestion order is deterministic.
    raise NotImplementedError("Implement load_documents()")


def chunk_documents(documents, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split each document into overlapping character chunks and attach metadata.

    Args:
        documents: List of dicts from load_documents().
        chunk_size: Maximum characters per chunk.
        overlap: Characters of shared context between consecutive chunks.

    Returns:
        List of chunk dicts with keys: text, source, chunk_id.
    """
    # TODO: For each doc, walk text[start:start+chunk_size] with step chunk_size-overlap.
    #   Append {"text": chunk, "source": doc["filename"], "chunk_id": n}.
    raise NotImplementedError("Implement chunk_documents()")


def embed_chunks(chunks):
    """Embed the text of every chunk in a single litellm call.

    Args:
        chunks: List of chunk dicts (must have a "text" key).

    Returns:
        numpy array of shape (N, D), dtype float32.
    """
    # TODO: Extract chunk["text"] for all chunks, call litellm.embedding(),
    #   and return a numpy float32 array.
    raise NotImplementedError("Implement embed_chunks()")


def build_index(vectors):
    """Create and populate a FAISS IndexFlatL2 from a numpy array of vectors.

    Args:
        vectors: numpy array of shape (N, D), dtype float32.

    Returns:
        faiss.IndexFlatL2 containing all N vectors.
    """
    # TODO: Read the dimension from vectors.shape[1], construct the index,
    #   and call index.add(vectors).
    raise NotImplementedError("Implement build_index()")


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
    # TODO: Embed [query] with litellm, reshape to (1, D) float32,
    #   call index.search(), and return chunks[idx] for each idx in indices[0].
    raise NotImplementedError("Implement retrieve()")


def build_rag_prompt(query, retrieved_chunks):
    """Format the retrieved context into a prompt ready for get_completion.

    Args:
        query: User question string.
        retrieved_chunks: List of chunk dicts from retrieve().

    Returns:
        List of message dicts: [{"role": "system", ...}, {"role": "user", ...}]
    """
    # TODO: Join the chunks with "---" separators, each prefixed with
    #   "[Source: <source>]". Build a user message with the context block
    #   followed by the question.
    raise NotImplementedError("Implement build_rag_prompt()")


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
    # docs = load_documents(KB_DIR)
    # print(f"  Loaded {len(docs)} documents: {[d['filename'] for d in docs]}")

    # print("Chunking documents...")
    # chunks = chunk_documents(docs)
    # print(f"  Created {len(chunks)} chunks")

    # print("Embedding chunks...")
    # vectors = embed_chunks(chunks)
    # print(f"  Vectors shape: {vectors.shape}")

    # print("Building FAISS index...")
    # index = build_index(vectors)
    # print(f"  Index ready: {index.ntotal} vectors\n")

    # for query in SAMPLE_QUERIES:
    #     print(f"Q: {query}")
    #     result = rag_query(query, index, chunks)
    #     print(f"A: {result['answer'].strip()}")
    #     print(f"   Sources: {result['sources']}")
    #     print()


if __name__ == "__main__":
    main()
