# Exercise: Eval Harness

**Chapter 8: Prompt Iteration & Evaluation**

**Goal:** Build a reusable evaluation framework: a golden dataset of input/expected pairs, a scoring function, and a `run_eval()` harness that reports pass rate and failing cases.

**Skills practiced:**
- Designing a golden dataset with edge cases
- Writing a keyword/substring scoring function
- Interpreting pass rate to guide prompt iteration

## Instructions

1. Go to the `start/` directory and open `eval_harness.py`.
2. Read `GOLDEN_DATASET` and understand the `expected_category` values.
3. Complete `score_response()` to check whether the model's output contains the expected category as a substring (case-insensitive).
4. Complete `run_eval()` to iterate over the dataset, call the `prompt_fn` for each input, score each result, and return `(pass_rate, failing_cases)`.
5. Run the file to see the baseline prompt's accuracy:
   ```bash
   python exercises/ch08/eval_harness/start/eval_harness.py
   ```
6. **Optional:** edit `SYSTEM_PROMPT` to improve accuracy and re-run.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
