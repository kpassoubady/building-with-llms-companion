# Exercise: Mini Evaluation Harness

**Chapter 14: Ethics, Bias and Evaluation**

**Goal:** Build a mini evaluation harness with a golden dataset, keyword-based scoring, pass-rate reporting, and a `check_for_drift` function that flags regressions when one prompt version performs worse than another.

**Skills practiced:**
- Defining a golden dataset with expected keywords
- Keyword-based automated scoring of LLM responses
- Summarising pass rate and identifying the worst-performing test case
- Drift detection by comparing two sets of evaluation results

## Instructions

1. Go to the `start/` directory and open `eval_harness.py`.
2. Review `GOLDEN_DATASET` - five test cases each with a `prompt`, a list of `expected_keywords` that must appear in the response, and an optional list of `forbidden_keywords` that must NOT appear.
3. Implement `evaluate_response(response, test_case)` which returns a dict with keys `passed` (bool), `score` (0.0-1.0), and `missing` (list of missing expected keywords).
4. Implement `run_evaluation(system_prompt="")` which calls `get_completion` for every case in `GOLDEN_DATASET`, scores each response, and returns a list of result dicts (one per case, including the case itself and the raw response).
5. Implement `check_for_drift(results_a, results_b, threshold=0.05)` that computes the pass rate for each result set and prints a warning if `results_b` is more than threshold below `results_a`.
6. In `main()`: run two evaluations (`SYSTEM_PROMPT_A` and `SYSTEM_PROMPT_B`), print a summary table, then call `check_for_drift` to compare them.
7. Run the file:
   ```bash
   python exercises/ch14/eval_harness/start/eval_harness.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
