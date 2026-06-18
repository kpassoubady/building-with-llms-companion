# Exercise: Prompt Rewriter

**Chapter 5: Prompt Engineering Fundamentals**

**Goal:** Fix 5 deliberately bad prompts by rewriting each one using the 4 building blocks (Instruction, Context, Input Data, Output Format), then run both versions and compare the outputs side-by-side.

**Skills practiced:**
- Recognising common prompt anti-patterns
- Applying all 4 building blocks to a real rewrite
- Comparing model outputs to see the quality difference

## Instructions

1. Go to the `start/` directory and open `prompt_rewriter.py`.
2. Read `BAD_PROMPTS`. Each entry describes what is wrong with the prompt.
3. For each entry, complete the "rewritten" field in `REWRITES` using all 4 building blocks. Keep the same underlying topic as the bad prompt.
4. Complete `run_comparison()` to call the model with both versions and print the responses side-by-side.
5. Run the file and note how much the rewrite improves output quality:
   ```bash
   python exercises/ch05/prompt_rewriter/start/prompt_rewriter.py
   ```
6. (Stretch) Add a sixth entry of your own, with a bad prompt you have actually written before.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
