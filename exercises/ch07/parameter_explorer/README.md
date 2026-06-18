# Exercise: Parameter Explorer

**Chapter 7: API Parameters & Output Control**

**Goal:** Build an interactive tool that lets you set API parameters via prompts, send a user message, and immediately see how the output changes.

**Skills practiced:**
- Reading and validating user input with sensible defaults
- Passing temperature, top_p, max_tokens, stop, presence_penalty, frequency_penalty, and seed to get_completion
- Observing the effect of each parameter on model output
- Using seed to reproduce identical outputs for comparison

## Instructions

1. Go to the `start/` directory and open `parameter_explorer.py`.
2. Implement `collect_parameters()` to read each parameter from stdin.
3. Implement `run_with_parameters()` to call `get_completion_full()` with those params.
4. Run the file and experiment:
   ```bash
   python exercises/ch07/parameter_explorer/start/parameter_explorer.py
   ```
5. Try `seed=42` twice to see reproducibility.
6. Try `stop=[".", "!"]` to see how the response truncates.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
