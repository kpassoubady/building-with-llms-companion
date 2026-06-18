# Exercise: Code Explainer

**Chapter 4: Model Capabilities & Limitations**

**Goal:** Use an LLM to produce a plain-English explanation of an unfamiliar Python function, practising the system+user message pattern.

**Skills practiced:**
- Constructing system and user messages
- Using `tier="mini"` for a reliable, answer-in-prompt task
- Interpreting LLM output for code explanation

## Instructions

1. Go to the `start/` directory and open `code_explainer.py`.
2. Read `SAMPLE_CODE` and understand what the function does.
3. Complete `explain_code()` so it sends a system message defining the expert persona and a user message containing the code.
4. Run the file and read the explanation the model returns:
   ```bash
   python exercises/ch04/code_explainer/start/code_explainer.py
   ```
5. Try swapping `SAMPLE_CODE` for a function of your own.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
