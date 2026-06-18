import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import numpy as np
import litellm  # noqa: E402 - used directly for embedding calls

# NOTE: embedding model name may need adjusting per provider.
# OpenAI: "text-embedding-3-small" | Google: "gemini/text-embedding-004"
EMBEDDING_MODEL = "text-embedding-3-small"

# ---------------------------------------------------------------------------
# Guard against missing optional dependencies
# ---------------------------------------------------------------------------

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("faiss-cpu is not installed. Run: pip install faiss-cpu")

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("chromadb is not installed. Run: pip install chromadb")

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

DOCUMENTS = [
    {
        "id": "doc-0",
        "source": "python-intro.md",
        "text": (
            "Python is a high-level, interpreted programming language known for "
            "its clear syntax and broad standard library. It supports multiple "
            "programming paradigms including procedural, object-oriented, and "
            "functional styles."
        ),
    },
    {
        "id": "doc-1",
        "source": "faiss-overview.md",
        "text": (
            "FAISS (Facebook AI Similarity Search) is a library for efficient "
            "similarity search over dense vectors. It provides several index "
            "types optimised for different speed-accuracy trade-offs and can "
            "search billions of vectors in milliseconds."
        ),
    },
    {
        "id": "doc-2",
        "source": "chroma-overview.md",
        "text": (
            "Chroma is an open-source vector database that stores documents, "
            "metadata, and embeddings together. It provides a simple Python API "
            "and can auto-embed text using a configured embedding function, "
            "making it easy to prototype semantic search applications."
        ),
    },
    {
        "id": "doc-3",
        "source": "rag-basics.md",
        "text": (
            "Retrieval-Augmented Generation (RAG) combines a retriever with a "
            "language model. The retriever finds relevant document chunks from a "
            "vector store; the generator reads those chunks and produces a "
            "grounded answer, reducing hallucinations compared to pure LLM calls."
        ),
    },
    {
        "id": "doc-4",
        "source": "embeddings-basics.md",
        "text": (
            "Text embeddings are fixed-length vectors that capture semantic "
            "meaning. Texts with similar meaning produce vectors that are close "
            "in the vector space, which is measured using cosine similarity or "
            "Euclidean distance. Embedding models range from 384 to 3072 dimensions."
        ),
    },
]

QUERY = "How does FAISS perform similarity search over vectors?"

# ---------------------------------------------------------------------------
# Shared embedding helper
# ---------------------------------------------------------------------------


def embed_texts(texts):
    """Embed a list of strings via litellm.embedding."""
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=texts)
    vectors = [item["embedding"] for item in resp["data"]]
    return np.array(vectors, dtype=np.float32)


# ---------------------------------------------------------------------------
# FAISS functions
# ---------------------------------------------------------------------------


def build_faiss_index(documents):
    """Embed DOCUMENTS and store vectors in a FAISS IndexFlatL2."""
    texts = [doc["text"] for doc in documents]
    vectors = embed_texts(texts)
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index, documents


def search_faiss(query, index, metadata, k=3):
    """Embed the query and retrieve top-k results from the FAISS index."""
    q_vec = embed_texts([query])
    distances, indices = index.search(q_vec, k)
    results = []
    for rank, idx in enumerate(indices[0]):
        doc = metadata[idx]
        results.append({
            "source": doc["source"],
            "text": doc["text"],
            "distance": float(distances[0][rank]),
        })
    return results


# ---------------------------------------------------------------------------
# Chroma functions
# ---------------------------------------------------------------------------


def build_chroma_collection(documents):
    """Add DOCUMENTS to an in-memory Chroma collection with metadata."""
    client = chromadb.Client()
    collection = client.create_collection("docs")
    vectors = embed_texts([doc["text"] for doc in documents])
    collection.add(
        ids=[doc["id"] for doc in documents],
        documents=[doc["text"] for doc in documents],
        metadatas=[{"source": doc["source"]} for doc in documents],
        embeddings=vectors.tolist(),
    )
    return collection


def search_chroma(query, collection, k=3):
    """Query the Chroma collection and return top-k results."""
    # Since we passed custom embeddings when building the collection, we must also
    # embed the query using the exact same model to perform a fair comparison.
    q_vec = embed_texts([query])
    results = collection.query(
        query_embeddings=q_vec.tolist(),
        n_results=k
    )
    
    output = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        output.append({"source": meta["source"], "text": text, "distance": dist})
    return output


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def print_results(results, label):
    print(f"\n{label}")
    print("-" * 60)
    for i, r in enumerate(results, 1):
        print(f"  #{i}  [{r['source']}]  dist={r['distance']:.4f}")
        print(f"       {r['text'][:80]}...")


def main():
    print("Chapter 10 - Vector DB Comparison\n")
    print(f"Query: {QUERY!r}\n")

    if FAISS_AVAILABLE:
        print("Building FAISS index...")
        faiss_index, faiss_meta = build_faiss_index(DOCUMENTS)
        faiss_results = search_faiss(QUERY, faiss_index, faiss_meta, k=3)
        print_results(faiss_results, "FAISS results (L2 distance - lower is better)")
    else:
        print("Skipping FAISS (not installed).")

    if CHROMA_AVAILABLE:
        print("\nBuilding Chroma collection...")
        collection = build_chroma_collection(DOCUMENTS)
        chroma_results = search_chroma(QUERY, collection, k=3)
        print_results(chroma_results, "Chroma results (distance - lower is better)")
    else:
        print("Skipping Chroma (not installed).")

    print("\nObservations:")
    print("  - FAISS: you manage metadata in a parallel Python list.")
    print("  - Chroma: metadata is stored alongside vectors in the collection.")
    print("  - Both return the same top document for the same query (if using")
    print("    the same embedding model).")


if __name__ == "__main__":
    main()
