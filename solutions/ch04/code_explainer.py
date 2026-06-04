"""
Exercise: Code Explainer
Chapter 4: Model Capabilities & Limitations

Goal: Use an LLM to produce a plain-English explanation of an unfamiliar
Python function, practising the system+user message pattern.

Skills practiced:
- Constructing system and user messages
- Using tier="mini" for a reliable, answer-in-prompt task
- Interpreting LLM output for code explanation

Instructions:
1. Read SAMPLE_CODE and understand what the function does.
2. Complete explain_code() so it sends a system message defining the expert
   persona and a user message containing the code.
3. Run the file and read the explanation the model returns.
4. Try swapping SAMPLE_CODE for a function of your own.

Run: python solutions/ch04/code_explainer.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_CODE = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
"""


# ---------------------------------------------------------------------------
# Solution
# ---------------------------------------------------------------------------


def explain_code(code: str) -> str:
    """Return a plain-English explanation of the given Python code snippet.

    Args:
        code: A string containing one or more Python functions.

    Returns:
        A string with the model's plain-English explanation.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior Python developer. "
                "Explain the given function's purpose, parameters, "
                "return value, and time complexity in 3-5 sentences. "
                "Use plain language suitable for a junior engineer."
            ),
        },
        {
            "role": "user",
            "content": f"Explain this code:\n```python\n{code}\n```",
        },
    ]
    return get_completion(messages, tier="mini", temperature=0.3)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Code Explainer ===\n")
    print("Function under review:")
    print(SAMPLE_CODE)
    print("-" * 40)
    explanation = explain_code(SAMPLE_CODE)
    print("Explanation:")
    print(explanation)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Code Explainer ===
#
# Function under review:
# (the merge_sort function printed above)
# ----------------------------------------
# Explanation:
# merge_sort implements the classic divide-and-conquer sorting algorithm.
# It recursively splits the input list in half until each sub-list has
# one element, then merges the sorted halves back together by comparing
# elements one at a time. The function accepts a list and returns a new
# sorted list without modifying the original. Its time complexity is
# O(n log n) in all cases, making it efficient for large inputs.
