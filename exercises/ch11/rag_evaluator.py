"""
Exercise: RAG Evaluator
Chapter 11: Retrieval-Augmented Generation (RAG)

Goal: Run a small evaluation set through the RAG pipeline and compute two
metrics: retrieval recall (did the expected source appear in the top-k results?)
and answer accuracy (do the answer keywords appear in the generated text?).

Skills practiced:
- Systematic RAG evaluation with a labelled eval set
- Retrieval recall: expected_source in top-k sources
- Answer accuracy: checking for expected keyword coverage
- Printing a structured evaluation report

Instructions:
1. Run build_pipeline() to load, chunk, embed, and index the knowledge base.
2. Implement evaluate_retrieval() to count how many queries surface the expected
   source in the top-k results.
3. Implement evaluate_answer() to run the full RAG query and check how many
   expected keywords appear in the answer (case-insensitive).
4. Implement run_evaluation() to loop over EVAL_SET, call both evaluators, and
   collect per-question results.
5. Run main() and review the printed report. Which questions fail? Why?

Run: python exercises/ch11/rag_evaluator.py  (from the repo root)
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

KB_DIR = os.path.join(os.path.dirname(__file__), "knowledge-base")
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
# Evaluation set
# Each entry: question, expected_source, expected_keywords
# ---------------------------------------------------------------------------

EVAL_SET = [
    {
        "question": "What happens if a payment fails?",
        "expected_source": "billing-faq.md",
        "expected_keywords": ["retry", "suspended", "14"],
    },
    {
        "question": "How do I cancel my subscription?",
        "expected_source": "billing-faq.md",
        "expected_keywords": ["cancel", "billing period", "settings"],
    },
    {
        "question": "Can I get a refund on a monthly plan?",
        "expected_source": "billing-faq.md",
        "expected_keywords": ["non-refundable", "7 days", "annual"],
    },
    {
        "question": "What training must new employees finish in the first 30 days?",
        "expected_source": "onboarding.md",
        "expected_keywords": ["security", "code of conduct", "data privacy"],
    },
    {
        "question": "How long does it take to get access to production systems?",
        "expected_source": "onboarding.md",
        "expected_keywords": ["three days", "manager", "approve"],
    },
    {
        "question": "What is the meal allowance for business travel?",
        "expected_source": "onboarding.md",
        "expected_keywords": ["75", "per day", "travel"],
    },
]

# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------


def build_pipeline(docs_dir=KB_DIR):
    """Load, chunk, embed, and index the knowledge base.

    Returns:
        (faiss.Index, list[dict]) - index and parallel chunk metadata list.
    """
    documents = []
    for fname in sorted(os.listdir(docs_dir)):
        if fname.endswith(".md"):
            fpath = os.path.join(docs_dir, fname)
            with open(fpath, "r") as f:
                documents.append({"filename": fname, "content": f.read()})

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

    texts = [c["text"] for c in chunks]
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=texts)
    vectors = np.array(
        [item["embedding"] for item in resp["data"]],
        dtype=np.float32,
    )
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index, chunks


def retrieve(query, index, chunks, k=TOP_K):
    """Return top-k chunk dicts for the given query."""
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=[query])
    q_vec = np.array([resp["data"][0]["embedding"]], dtype=np.float32)
    distances, indices = index.search(q_vec, k)
    return [chunks[i] for i in indices[0]]


def rag_query(query, index, chunks):
    """Retrieve top-k chunks and generate a cited answer.

    Returns:
        Dict with keys: answer (str), sources (list[str]).
    """
    retrieved = retrieve(query, index, chunks)
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in retrieved
    )
    messages = [
        {"role": "system", "content": RAG_SYSTEM},
        {
            "role": "user",
            "content": f"Context:\n{context}\n\n---\n\nQuestion: {query}",
        },
    ]
    answer = get_completion(messages, temperature=0.0)
    sources = list(dict.fromkeys(c["source"] for c in retrieved))
    return {"answer": answer, "sources": sources}


# ---------------------------------------------------------------------------
# Evaluation functions
# ---------------------------------------------------------------------------


def evaluate_retrieval(query, expected_source, index, chunks, k=TOP_K):
    """Check whether expected_source appears among the top-k retrieved sources.

    Args:
        query: Question string.
        expected_source: Filename that should contain the answer.
        index: FAISS index.
        chunks: Parallel metadata list.
        k: Number of chunks to retrieve.

    Returns:
        True if expected_source is in the retrieved sources, False otherwise.
    """
    # TODO: Call retrieve(), collect the unique source filenames, and return
    #   True if expected_source is in that set.
    # Hint:
    # retrieved = retrieve(query, index, chunks, k)
    # retrieved_sources = {c["source"] for c in retrieved}
    # return expected_source in retrieved_sources
    raise NotImplementedError("Implement evaluate_retrieval()")


def evaluate_answer(answer, expected_keywords):
    """Compute the fraction of expected keywords that appear in the answer.

    Args:
        answer: Generated answer string.
        expected_keywords: List of strings that should appear (case-insensitive).

    Returns:
        Float in [0.0, 1.0] - fraction of keywords found.
    """
    # TODO: Lowercase the answer, then count how many keywords are substrings of it.
    #   Return found / len(expected_keywords).  Guard against an empty keyword list.
    # Hint:
    # if not expected_keywords:
    #     return 1.0
    # lower = answer.lower()
    # found = sum(1 for kw in expected_keywords if kw.lower() in lower)
    # return found / len(expected_keywords)
    raise NotImplementedError("Implement evaluate_answer()")


def run_evaluation(eval_set, index, chunks):
    """Run every eval case through the pipeline and collect results.

    Args:
        eval_set: List of dicts with question, expected_source, expected_keywords.
        index: FAISS index.
        chunks: Parallel metadata list.

    Returns:
        List of result dicts with keys:
          question, retrieval_hit (bool), keyword_score (float), answer (str).
    """
    # TODO: For each case in eval_set:
    #   1. Call evaluate_retrieval() -> retrieval_hit
    #   2. Call rag_query() to get the answer
    #   3. Call evaluate_answer() -> keyword_score
    #   4. Append a result dict and print a one-line progress indicator.
    # Hint:
    # results = []
    # for i, case in enumerate(eval_set, 1):
    #     print(f"  [{i}/{len(eval_set)}] {case['question'][:55]}...")
    #     retrieval_hit = evaluate_retrieval(
    #         case["question"], case["expected_source"], index, chunks
    #     )
    #     result = rag_query(case["question"], index, chunks)
    #     keyword_score = evaluate_answer(result["answer"], case["expected_keywords"])
    #     results.append({
    #         "question": case["question"],
    #         "retrieval_hit": retrieval_hit,
    #         "keyword_score": keyword_score,
    #         "answer": result["answer"],
    #     })
    # return results
    raise NotImplementedError("Implement run_evaluation()")


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_report(results):
    """Print a formatted evaluation summary."""
    total = len(results)
    retrieval_hits = sum(1 for r in results if r["retrieval_hit"])
    avg_keyword = sum(r["keyword_score"] for r in results) / total if total else 0.0

    print("\n" + "=" * 72)
    print(f"{'QUESTION':44}  {'RETRIEVAL':9}  {'KEYWORDS':8}")
    print("=" * 72)
    for r in results:
        retrieval_label = "HIT " if r["retrieval_hit"] else "MISS"
        kw_label = f"{r['keyword_score']:.0%}"
        print(f"  {r['question'][:44]:44}  {retrieval_label:9}  {kw_label:8}")

    print("=" * 72)
    print(
        f"Retrieval recall: {retrieval_hits}/{total} "
        f"({retrieval_hits / total:.0%})   "
        f"Avg keyword score: {avg_keyword:.0%}"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 11 - RAG Evaluator\n")

    print(f"Building pipeline from {KB_DIR}...")
    index, chunks = build_pipeline()
    print(f"  {index.ntotal} vectors indexed\n")

    print("Running evaluation set...")
    results = run_evaluation(EVAL_SET, index, chunks)

    print_report(results)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# Chapter 11 - RAG Evaluator
#
# Building pipeline from .../knowledge-base...
#   11 vectors indexed
#
# Running evaluation set...
#   [1/6] What happens if a payment fails?...
#   [2/6] How do I cancel my subscription?...
#   ...
#
# ========================================================================
# QUESTION                                      RETRIEVAL  KEYWORDS
# ========================================================================
#   What happens if a payment fails?            HIT        100%
#   How do I cancel my subscription?            HIT        100%
#   Can I get a refund on a monthly plan?       HIT         67%
#   What training must new employees finish...  HIT        100%
#   How long does it take to get access to...   HIT         67%
#   What is the meal allowance for busines...   HIT        100%
# ========================================================================
# Retrieval recall: 6/6 (100%)   Avg keyword score: 89%
