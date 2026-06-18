import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

REVIEWS = [
    "This product is absolutely amazing!",
    "The design is gorgeous but the software is buggy.",
    "It works as described. Nothing special.",
    "Not worth the price. There are better alternatives.",
    "Pretty good but the battery could last longer.",
    "Completely broken on arrival. Terrible experience.",
    "Exceeded my expectations in every way.",
    "Decent build quality, average performance.",
    "Support team was unhelpful and rude.",
    "Nice packaging but the item itself is mediocre.",
]

FEW_SHOT_EXAMPLES = [
    ("Absolutely love it, best purchase this year!", "POSITIVE"),
    ("Stopped working after two days. Very disappointed.", "NEGATIVE"),
    ("Does the job. No complaints, no praise.", "NEUTRAL"),
]


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def classify_zero_shot(reviews):
    """Classify each review using a zero-shot prompt."""
    results = []
    for review in reviews:
        label = get_completion(
            messages=[
                {"role": "system", "content": "Classify as POSITIVE, NEGATIVE, or NEUTRAL. "
                    "Respond with ONLY the label."},
                {"role": "user", "content": review},
            ],
            tier="mini",
            temperature=0.0,
        )
        results.append((review, label.strip()))
    return results


def classify_few_shot(reviews):
    """Classify each review using a few-shot prompt with labeled examples."""
    example_block = "\n".join(
        f"Review: {text}\nLabel: {label}" for text, label in FEW_SHOT_EXAMPLES
    )
    system = (
        "Classify the sentiment of a product review as POSITIVE, NEGATIVE, or NEUTRAL.\n\n"
        "Examples:\n" + example_block + "\n\nRespond with ONLY the label."
    )
    results = []
    for review in reviews:
        label = get_completion(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": review},
            ],
            tier="mini",
            temperature=0.0,
        )
        results.append((review, label.strip()))
    return results


def compare_strategies(reviews):
    """Run both strategies and print a side-by-side comparison."""
    print("Running zero-shot classifier...")
    zero_results = classify_zero_shot(reviews)

    print("Running few-shot classifier...")
    few_results = classify_few_shot(reviews)

    print("\n" + "=" * 70)
    print(f"{'ZERO-SHOT':10}  {'FEW-SHOT':10}  REVIEW")
    print("=" * 70)
    for (review, zero_label), (_, few_label) in zip(zero_results, few_results):
        match = "   " if zero_label == few_label else "(*)"
        print(f"{zero_label:10}  {few_label:10}  {review[:45]}  {match}")

    diffs = sum(1 for (_, z), (_, f) in zip(zero_results, few_results) if z != f)
    print("=" * 70)
    print(f"Differences: {diffs} / {len(reviews)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 6 - Sentiment Classifier\n")
    compare_strategies(REVIEWS)


if __name__ == "__main__":
    main()
