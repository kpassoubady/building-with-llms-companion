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
    """Classify each review using a zero-shot prompt.

    Args:
        reviews: List of review strings to classify.

    Returns:
        List of (review, label) tuples.
    """
    # TODO: For each review, call get_completion with:
    #   - system: instruct the model to classify as POSITIVE, NEGATIVE, or NEUTRAL
    #             and respond with ONLY the label
    #   - user: the review text
    #   - tier="mini", temperature=0.0
    raise NotImplementedError("Implement classify_zero_shot()")


def classify_few_shot(reviews):
    """Classify each review using a few-shot prompt with labeled examples.

    Args:
        reviews: List of review strings to classify.

    Returns:
        List of (review, label) tuples.
    """
    # TODO: Build a system message that includes the FEW_SHOT_EXAMPLES above.
    #   Format each example as:
    #     Review: <text>
    #     Label: <label>
    #   Append a clear instruction to only output the label for the new review.
    #   Then loop over reviews exactly as in classify_zero_shot().
    raise NotImplementedError("Implement classify_few_shot()")


def compare_strategies(reviews):
    """Run both strategies and print a side-by-side comparison."""
    print("Running zero-shot classifier...")
    # zero_results = classify_zero_shot(reviews)

    print("Running few-shot classifier...")
    # few_results = classify_few_shot(reviews)

    print("\n" + "=" * 70)
    print(f"{'ZERO-SHOT':10}  {'FEW-SHOT':10}  REVIEW")
    print("=" * 70)
    # for (review, zero_label), (_, few_label) in zip(zero_results, few_results):
    #     match = "   " if zero_label == few_label else "(*)"
    #     print(f"{zero_label:10}  {few_label:10}  {review[:45]}  {match}")

    # diffs = sum(1 for (_, z), (_, f) in zip(zero_results, few_results) if z != f)
    print("=" * 70)
    # print(f"Differences: {diffs} / {len(reviews)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 6 - Sentiment Classifier\n")
    compare_strategies(REVIEWS)


if __name__ == "__main__":
    main()
