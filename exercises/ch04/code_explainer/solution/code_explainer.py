import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
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
# Exercise function
# ---------------------------------------------------------------------------


def explain_code(code: str) -> str:
    """Return a plain-English explanation of the given Python code snippet."""
    messages = [
        {"role": "system",
         "content": "You are a senior Python developer. "
             "Explain the given function's purpose, parameters, "
             "return value, and time complexity in 3-5 sentences. "
             "Use plain language suitable for a junior engineer."},
        {"role": "user",
         "content": f"Explain this code:\n```python\n{code}\n```"},
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
