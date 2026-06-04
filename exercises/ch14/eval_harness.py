"""
Exercise: Mini Evaluation Harness
Chapter 14: Ethics, Bias and Evaluation

Goal: Build a mini evaluation harness with a golden dataset, keyword-based
scoring, pass-rate reporting, and a check_for_drift function that flags
regressions when one prompt version performs worse than another.

Skills practiced:
- Defining a golden dataset with expected keywords
- Keyword-based automated scoring of LLM responses
- Summarising pass rate and identifying the worst-performing test case
- Drift detection by comparing two sets of evaluation results

Instructions:
1. Review GOLDEN_DATASET - five test cases each with a "prompt", a list of
   "expected_keywords" that must appear in the response, and an optional list
   of "forbidden_keywords" that must NOT appear.
2. Implement evaluate_response(response, test_case) which returns a dict with
   keys "passed" (bool), "score" (0.0-1.0), and "missing" (list of missing
   expected keywords).
3. Implement run_evaluation(system_prompt="") which calls get_completion for
   every case in GOLDEN_DATASET, scores each response, and returns a list of
   result dicts (one per case, including the case itself and the raw response).
4. Implement check_for_drift(results_a, results_b, threshold=0.05) that
   computes the pass rate for each result set and prints a warning if
   results_b is more than threshold below results_a.
5. In main(): run two evaluations (SYSTEM_PROMPT_A and SYSTEM_PROMPT_B),
   print a summary table, then call check_for_drift to compare them.

Run: python exercises/ch14/eval_harness.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Golden dataset - five cases covering core Q&A scenarios
# ---------------------------------------------------------------------------
GOLDEN_DATASET = [
    {
        "id": "py-list-vs-tuple",
        "prompt": "In one sentence, what is the key difference between a Python list and a tuple?",
        "expected_keywords": ["mutable", "immutable"],
        "forbidden_keywords": [],
    },
    {
        "id": "py-exception-handling",
        "prompt": "Name the two keywords used to handle exceptions in Python.",
        "expected_keywords": ["try", "except"],
        "forbidden_keywords": [],
    },
    {
        "id": "py-dict-lookup",
        "prompt": "What is the average time complexity of a dictionary lookup in Python?",
        "expected_keywords": ["O(1)", "constant"],
        "forbidden_keywords": ["O(n)", "linear"],
    },
    {
        "id": "git-commit",
        "prompt": "What git command saves staged changes to the local repository?",
        "expected_keywords": ["git commit"],
        "forbidden_keywords": [],
    },
    {
        "id": "api-rest-status",
        "prompt": "What HTTP status code indicates a successful POST that created a resource?",
        "expected_keywords": ["201"],
        "forbidden_keywords": ["200", "404"],
    },
]

# Two system prompts to compare - A is concise, B is verbose and potentially noisier
SYSTEM_PROMPT_A = "Answer the user's question accurately and concisely."
SYSTEM_PROMPT_B = (
    "You are an extremely helpful assistant. "
    "Please provide a thorough, detailed, comprehensive explanation "
    "with background context, examples, and caveats for every answer you give."
)


# ---------------------------------------------------------------------------
# Step 1: Score a single response against a test case
# ---------------------------------------------------------------------------
def evaluate_response(response, test_case):
    """Score a response against expected and forbidden keywords.

    Args:
        response: String returned by the LLM.
        test_case: One entry from GOLDEN_DATASET.

    Returns:
        Dict with keys:
          "passed"  - True if all expected keywords found and none forbidden
          "score"   - float 0.0-1.0 (fraction of expected keywords present)
          "missing" - list of expected keywords absent from the response

    Hint:
    #   lower = response.lower()
    #   found = [k for k in test_case["expected_keywords"] if k.lower() in lower]
    #   missing = [k for k in test_case["expected_keywords"] if k.lower() not in lower]
    #   forbidden_hit = any(f.lower() in lower for f in test_case.get("forbidden_keywords", []))
    #   total = len(test_case["expected_keywords"])
    #   score = len(found) / total if total else 1.0
    #   passed = (len(missing) == 0) and (not forbidden_hit)
    #   return {"passed": passed, "score": score, "missing": missing}
    """
    # TODO: Implement evaluate_response.
    raise NotImplementedError("Implement evaluate_response")


# ---------------------------------------------------------------------------
# Step 2: Run full evaluation over GOLDEN_DATASET
# ---------------------------------------------------------------------------
def run_evaluation(system_prompt=""):
    """Run every GOLDEN_DATASET case through the LLM and score results.

    Args:
        system_prompt: Optional system message prepended to each request.

    Returns:
        List of dicts, one per test case, each containing:
          "id", "prompt", "response", "passed", "score", "missing"

    Hint:
    #   results = []
    #   for case in GOLDEN_DATASET:
    #       messages = []
    #       if system_prompt:
    #           messages.append({"role": "system", "content": system_prompt})
    #       messages.append({"role": "user", "content": case["prompt"]})
    #       response = get_completion(messages, tier="mini", temperature=0.0)
    #       scored = evaluate_response(response, case)
    #       results.append({
    #           "id": case["id"],
    #           "prompt": case["prompt"],
    #           "response": response,
    #           **scored,
    #       })
    #   return results
    """
    # TODO: Implement run_evaluation.
    raise NotImplementedError("Implement run_evaluation")


# ---------------------------------------------------------------------------
# Step 3: Drift detection
# ---------------------------------------------------------------------------
def check_for_drift(results_a, results_b, threshold=0.05):
    """Compare two evaluation result sets and flag a regression.

    A regression is flagged when the pass rate of results_b is more than
    threshold below the pass rate of results_a.

    Args:
        results_a: List of result dicts from run_evaluation (baseline).
        results_b: List of result dicts from run_evaluation (new prompt).
        threshold: Minimum acceptable drop in pass rate (default 0.05 = 5%).

    Returns:
        True if drift is detected, False otherwise.

    Hint:
    #   rate_a = sum(r["passed"] for r in results_a) / len(results_a)
    #   rate_b = sum(r["passed"] for r in results_b) / len(results_b)
    #   drop = rate_a - rate_b
    #   if drop > threshold:
    #       print(f"DRIFT DETECTED: pass rate dropped {drop:.1%} "
    #             f"({rate_a:.1%} -> {rate_b:.1%})")
    #       return True
    #   print(f"No significant drift (drop={drop:.1%}, threshold={threshold:.1%})")
    #   return False
    """
    # TODO: Implement check_for_drift.
    raise NotImplementedError("Implement check_for_drift")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _pass_rate(results):
    return sum(r["passed"] for r in results) / len(results)


def _worst_case(results):
    return min(results, key=lambda r: r["score"])


def _print_summary(label, results):
    print(f"\n--- {label} ---")
    print(f"{'ID':<25} {'Pass':>6} {'Score':>7}")
    print("-" * 42)
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"{r['id']:<25} {status:>6} {r['score']:>6.0%}")
    rate = _pass_rate(results)
    worst = _worst_case(results)
    print(f"\nPass rate: {rate:.0%}  |  Worst case: {worst['id']} (score {worst['score']:.0%})")
    if worst["missing"]:
        print(f"  Missing keywords: {worst['missing']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=== Evaluation Harness ===\n")

    print("Running evaluation with SYSTEM_PROMPT_A (concise)...")
    results_a = run_evaluation(system_prompt=SYSTEM_PROMPT_A)
    _print_summary("Prompt A - concise", results_a)

    print("\nRunning evaluation with SYSTEM_PROMPT_B (verbose)...")
    results_b = run_evaluation(system_prompt=SYSTEM_PROMPT_B)
    _print_summary("Prompt B - verbose", results_b)

    print("\n--- Drift detection ---")
    check_for_drift(results_a, results_b, threshold=0.05)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Evaluation Harness ===
#
# Running evaluation with SYSTEM_PROMPT_A (concise)...
#
# --- Prompt A - concise ---
# ID                        Pass   Score
# ------------------------------------------
# py-list-vs-tuple          PASS   100%
# py-exception-handling     PASS   100%
# py-dict-lookup            PASS   100%
# git-commit                PASS   100%
# api-rest-status           PASS   100%
#
# Pass rate: 100%  |  Worst case: py-list-vs-tuple (score 100%)
#
# Running evaluation with SYSTEM_PROMPT_B (verbose)...
# ...
#
# --- Drift detection ---
# No significant drift (drop=0.0%, threshold=5.0%)
#   -- or --
# DRIFT DETECTED: pass rate dropped 20.0% (100% -> 80%)
