"""
Exercise: Chunking Lab
Chapter 10: Embeddings & Vector Databases

Goal: Chunk a sample markdown document three ways, embed every chunk and a query,
then compare which strategy surfaces the most relevant chunk.

Skills practiced:
- Fixed-size chunking by character count
- Paragraph-boundary chunking (semantic split)
- Overlap chunking (fixed-size with shared context at boundaries)
- Embedding chunks and a query with litellm
- Scoring relevance by cosine similarity

Instructions:
1. Implement chunk_fixed() to split DOCUMENT by chunk_size characters (no overlap).
2. Implement chunk_by_paragraph() to split on blank lines, skipping empty strings.
3. Implement chunk_with_overlap() to split by chunk_size with an overlap step.
4. Implement embed_and_rank() to embed all chunks + the query, then return chunks
   sorted by cosine similarity to the query vector.
5. Run main() - which strategy returns the most relevant top chunk for QUERY?

Run: python exercises/ch10/chunking_lab.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
import litellm  # noqa: E402 - used directly for embedding calls

# NOTE: embedding model name may need adjusting per provider.
# OpenAI: "text-embedding-3-small" | Google: "gemini/text-embedding-004"
EMBEDDING_MODEL = "text-embedding-3-small"

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

DOCUMENT = """# Employee Handbook

## Welcome

Welcome to the company. We are glad you joined us and hope this handbook answers
your initial questions about policies and day-to-day life here.

## Working Hours

Standard working hours are 9 am to 5 pm, Monday through Friday. Flexible
arrangements can be discussed with your manager after the first 90 days.
Remote work is permitted up to three days per week for roles that allow it.

## Time Off

Full-time employees receive 20 days of paid vacation per year. Vacation accrues
at a rate of 1.67 days per month. Unused vacation may be carried over up to a
maximum of 10 days into the following year.

Sick leave is separate from vacation. Employees receive 10 sick days per year.
Sick days do not carry over and reset on January 1 each year.

Public holidays follow the standard calendar for the country of employment.
Employees working on a public holiday receive a substitute day off.

## Performance Reviews

Performance reviews are conducted twice a year: mid-year in June and year-end
in December. Managers provide written feedback and discuss development goals.
Salary adjustments, if any, take effect on the first of the month following
the year-end review.

## Code of Conduct

All employees are expected to treat colleagues, clients, and partners with
respect. Discrimination, harassment, and retaliation are strictly prohibited.
Violations should be reported to HR or through the anonymous ethics hotline.

## Benefits

The company offers health, dental, and vision insurance effective on your
start date. A 401(k) plan with 4% employer match is available after 90 days.
Employees also receive a $1,000 annual learning and development budget.
"""

QUERY = "How many vacation days do employees get and do they carry over?"

CHUNK_SIZE = 300
OVERLAP = 60

# ---------------------------------------------------------------------------
# Chunking functions
# ---------------------------------------------------------------------------


def chunk_fixed(text, chunk_size=CHUNK_SIZE):
    """Split text into non-overlapping fixed-size character chunks.

    Args:
        text: Source document string.
        chunk_size: Maximum characters per chunk.

    Returns:
        List of chunk strings.
    """
    # TODO: Walk the text in steps of chunk_size, slicing text[start:start+chunk_size].
    #   Stop when start >= len(text).
    # Hint:
    # chunks = []
    # start = 0
    # while start < len(text):
    #     chunks.append(text[start:start + chunk_size])
    #     start += chunk_size
    # return chunks
    raise NotImplementedError("Implement chunk_fixed()")


def chunk_by_paragraph(text):
    """Split text on blank lines (double newline), dropping empty chunks.

    Args:
        text: Source document string.

    Returns:
        List of non-empty paragraph strings.
    """
    # TODO: Split on "\n\n", strip each piece, and filter out empty strings.
    # Hint:
    # return [p.strip() for p in text.split("\n\n") if p.strip()]
    raise NotImplementedError("Implement chunk_by_paragraph()")


def chunk_with_overlap(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split text into fixed-size chunks with character overlap between them.

    Args:
        text: Source document string.
        chunk_size: Characters per chunk.
        overlap: Characters shared between consecutive chunks.

    Returns:
        List of chunk strings.
    """
    # TODO: Walk with step = chunk_size - overlap.  Each chunk is text[start:start+chunk_size].
    # Hint:
    # chunks, start = [], 0
    # step = chunk_size - overlap
    # while start < len(text):
    #     chunks.append(text[start:start + chunk_size])
    #     start += step
    # return chunks
    raise NotImplementedError("Implement chunk_with_overlap()")


# ---------------------------------------------------------------------------
# Embedding and ranking
# ---------------------------------------------------------------------------


def embed_texts(texts):
    """Embed a list of strings using litellm.

    Args:
        texts: List of strings.

    Returns:
        numpy array of shape (N, D), dtype float32.
    """
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=texts)
    vectors = [item["embedding"] for item in resp["data"]]
    return np.array(vectors, dtype=np.float32)


def cosine_scores(query_vec, chunk_vecs):
    """Return cosine similarity between a single query vector and each chunk vector.

    Args:
        query_vec: 1-D numpy array of shape (D,).
        chunk_vecs: 2-D numpy array of shape (N, D).

    Returns:
        1-D numpy array of shape (N,) with scores in [-1, 1].
    """
    q = query_vec / (np.linalg.norm(query_vec) + 1e-9)
    norms = np.linalg.norm(chunk_vecs, axis=1, keepdims=True) + 1e-9
    normed = chunk_vecs / norms
    return (normed @ q).astype(float)


def embed_and_rank(chunks, query):
    """Embed chunks and query, return chunks sorted by relevance descending.

    Args:
        chunks: List of chunk strings.
        query: Query string.

    Returns:
        List of (score, chunk_text) tuples, best match first.
    """
    # TODO: Embed all chunks + the query in a single call (append query to the list).
    #   Split off the last vector as the query vector.
    #   Compute cosine_scores(), zip with chunks, sort descending by score.
    # Hint:
    # all_texts = chunks + [query]
    # all_vecs = embed_texts(all_texts)
    # query_vec = all_vecs[-1]
    # chunk_vecs = all_vecs[:-1]
    # scores = cosine_scores(query_vec, chunk_vecs)
    # ranked = sorted(zip(scores, chunks), reverse=True)
    # return ranked
    raise NotImplementedError("Implement embed_and_rank()")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 10 - Chunking Lab\n")
    print(f"Query: {QUERY!r}\n")

    strategies = [
        ("Fixed-size",      chunk_fixed(DOCUMENT)),
        ("By-paragraph",    chunk_by_paragraph(DOCUMENT)),
        ("With-overlap",    chunk_with_overlap(DOCUMENT)),
    ]

    for name, chunks in strategies:
        print(f"--- {name} ({len(chunks)} chunks) ---")
        ranked = embed_and_rank(chunks, QUERY)
        score, top_chunk = ranked[0]
        print(f"  Top chunk (score={score:.3f}):")
        print(f"  {top_chunk[:120].strip()!r}")
        print()


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# Chapter 10 - Chunking Lab
#
# Query: 'How many vacation days do employees get and do they carry over?'
#
# --- Fixed-size (10 chunks) ---
#   Top chunk (score=0.847):
#   '## Time Off\n\nFull-time employees receive 20 days of paid vacation per year...'
#
# --- By-paragraph (9 chunks) ---
#   Top chunk (score=0.891):
#   'Full-time employees receive 20 days of paid vacation per year. Vacation accrues...'
#
# --- With-overlap (14 chunks) ---
#   Top chunk (score=0.863):
#   'Full-time employees receive 20 days of paid vacation per year. Vacation accrues...'
