import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import numpy as np
import litellm  # noqa: E402 - used directly for embedding calls

# NOTE: embedding model name may need adjusting per provider.
# OpenAI: "text-embedding-3-small" | Google: "gemini/text-embedding-004"
# Voyage: "voyage/voyage-3"
EMBEDDING_MODEL = "text-embedding-3-small"

# ---------------------------------------------------------------------------
# Sample data - 20 sentences across 4 topic clusters
# ---------------------------------------------------------------------------

SENTENCES = [
    # Programming (0-4)
    "Python uses indentation to define code blocks.",
    "A function in Python is defined with the def keyword.",
    "List comprehensions are a concise way to build lists in Python.",
    "Debugging is the process of finding and fixing errors in code.",
    "Unit tests verify that individual functions behave correctly.",
    # Machine learning (5-9)
    "Neural networks learn by adjusting weights through backpropagation.",
    "Training data is used to fit a model; test data evaluates it.",
    "Overfitting occurs when a model memorizes training data but fails on new data.",
    "Gradient descent minimizes the loss function during model training.",
    "Feature engineering transforms raw data into inputs a model can use.",
    # Cooking (10-14)
    "Sauteing vegetables in olive oil brings out their natural sweetness.",
    "Caramelization occurs when sugars are heated to high temperatures.",
    "A sharp knife makes prep work safer and faster in the kitchen.",
    "Blanching briefly boils vegetables, then shocks them in ice water.",
    "Seasoning with salt at each stage builds depth in a finished dish.",
    # Travel (15-19)
    "Booking flights early can save significant money on international trips.",
    "A carry-on bag lets you skip baggage claim and move faster through airports.",
    "Travel insurance covers medical emergencies and trip cancellations.",
    "Learning a few phrases in the local language is appreciated by residents.",
    "Jet lag is easier to manage when you adjust your sleep schedule before departure.",
]

# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def embed_sentences(sentences):
    """Embed a list of sentences and return their vectors as a 2-D numpy array."""
    resp = litellm.embedding(model=EMBEDDING_MODEL, input=sentences)
    vectors = [item["embedding"] for item in resp["data"]]
    return np.array(vectors, dtype=np.float32)


def cosine_similarity_matrix(vectors):
    """Compute pairwise cosine similarity for all sentence vectors."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normed = vectors / norms
    return normed @ normed.T


def find_top_pairs(sim_matrix, sentences, top_n=10):
    """Return the top-N most similar sentence pairs (excluding self-similarity)."""
    pairs = []
    n = len(sentences)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((float(sim_matrix[i, j]), sentences[i], sentences[j]))
    pairs.sort(reverse=True)
    return pairs[:top_n]


def print_cluster_summary(sim_matrix, sentences, threshold=0.70):
    """Print sentences that share at least one neighbor above the threshold."""
    print(f"\nSentences with a neighbor scoring >= {threshold}:")
    n = len(sentences)
    for i in range(n):
        neighbors = [
            sentences[j]
            for j in range(n)
            if i != j and sim_matrix[i, j] >= threshold
        ]
        if neighbors:
            print(f"  [{i:02d}] {sentences[i][:55]}")
            for nb in neighbors:
                print(f"        -> {nb[:55]}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 10 - Embedding Explorer\n")
    print(f"Embedding {len(SENTENCES)} sentences with {EMBEDDING_MODEL}...")

    vectors = embed_sentences(SENTENCES)
    print(f"Vectors shape: {vectors.shape}")

    sim_matrix = cosine_similarity_matrix(vectors)

    print("\nTop 10 most similar sentence pairs:")
    print("-" * 70)
    for score, sent_a, sent_b in find_top_pairs(sim_matrix, SENTENCES):
        print(f"  {score:.3f}  {sent_a[:45]!r}")
        print(f"         {sent_b[:45]!r}")

    print_cluster_summary(sim_matrix, SENTENCES, threshold=0.70)


if __name__ == "__main__":
    main()
