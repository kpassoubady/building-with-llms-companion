"""
Exercise: Eval Harness
Chapter 8: Prompt Iteration & Evaluation

Goal: Build a reusable evaluation framework: a golden dataset of
input/expected pairs, a scoring function, and a run_eval() harness
that reports pass rate and failing cases.

Skills practiced:
- Designing a golden dataset with edge cases
- Writing a keyword/substring scoring function
- Interpreting pass rate to guide prompt iteration

Instructions:
1. Read GOLDEN_DATASET and understand the expected_category values.
2. Complete score_response() to check whether the model's output contains
   the expected category as a substring (case-insensitive).
3. Complete run_eval() to iterate over the dataset, call the prompt_fn for
   each input, score each result, and return (pass_rate, failing_cases).
4. Run main() to see the baseline prompt's accuracy.
5. Optional: edit SYSTEM_PROMPT to improve accuracy and re-run.

Run: python solutions/ch08/eval_harness.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Golden dataset
# ---------------------------------------------------------------------------

GOLDEN_DATASET = [
    {
        "input": "The app crashes when I click save",
        "expected_category": "bug_report",
    },
    {
        "input": "Can you add dark mode?",
        "expected_category": "feature_request",
    },
    {
        "input": "I was charged twice this month",
        "expected_category": "billing",
    },
    {
        "input": "How do I export my data?",
        "expected_category": "how_to",
    },
    {
        "input": "My account is locked and I cannot log in",
        "expected_category": "account",
    },
    {
        "input": "The search results are completely wrong every time",
        "expected_category": "bug_report",
    },
    {
        "input": "I would love a keyboard shortcut for the dashboard",
        "expected_category": "feature_request",
    },
    {
        "input": "Where can I find my invoice from last quarter?",
        "expected_category": "billing",
    },
    {
        "input": "",
        "expected_category": "unknown",
    },
    {
        "input": "Hmm, I am not sure, something feels off",
        "expected_category": "unknown",
    },
]

SYSTEM_PROMPT = (
    "Classify the support message into exactly one category: "
    "bug_report, feature_request, billing, how_to, account, unknown. "
    "Reply with the category label only. No punctuation, no explanation."
)


# ---------------------------------------------------------------------------
# Solution functions
# ---------------------------------------------------------------------------


def score_response(response: str, expected_category: str) -> bool:
    """Return True if response contains the expected_category (case-insensitive).

    Args:
        response: The raw string returned by the model.
        expected_category: The label from the golden dataset entry.

    Returns:
        True when the response is considered correct, False otherwise.
    """
    return expected_category.lower() in response.strip().lower()


def run_eval(prompt_fn, dataset=GOLDEN_DATASET):
    """Run prompt_fn against every entry in dataset and return results.

    Args:
        prompt_fn: Callable(input_text: str) -> str. Calls the LLM.
        dataset: List of dicts with 'input' and 'expected_category' keys.

    Returns:
        Tuple of (pass_rate: float, failing_cases: list[dict]).
        pass_rate is 0.0-1.0. Each failing case dict has keys:
        'input', 'expected', 'actual'.
    """
    correct = 0
    failing_cases = []
    for entry in dataset:
        actual = prompt_fn(entry["input"])
        passed = score_response(actual, entry["expected_category"])
        if passed:
            correct += 1
        else:
            failing_cases.append({
                "input": entry["input"],
                "expected": entry["expected_category"],
                "actual": actual.strip(),
            })
    return correct / len(dataset), failing_cases


def classify(text: str) -> str:
    """Classify a single support message using SYSTEM_PROMPT."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text if text else "(empty message)"},
    ]
    return get_completion(messages, tier="mini", temperature=0.0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Eval Harness ===\n")
    print(f"Dataset size: {len(GOLDEN_DATASET)} entries")
    print(f"System prompt: {SYSTEM_PROMPT}\n")
    print("Running evaluation...")

    pass_rate, failing = run_eval(classify)

    print(f"\nPass rate: {pass_rate:.0%} ({int(pass_rate * len(GOLDEN_DATASET))}/{len(GOLDEN_DATASET)})\n")

    if failing:
        print("Failing cases:")
        for case in failing:
            label = case["input"][:50] or "(empty)"
            print(f"  FAIL | expected={case['expected']!r:15} actual={case['actual']!r:15} | {label}")
    else:
        print("All cases passed.")


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Eval Harness ===
#
# Dataset size: 10 entries
# System prompt: Classify the support message ...
#
# Running evaluation...
#
# Pass rate: 90% (9/10)
#
# Failing cases:
#   FAIL | expected='unknown'       actual='how_to'         | Hmm, I am not sure, ...
