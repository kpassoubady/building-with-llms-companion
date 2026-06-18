# Exercise: Bug Triager

**Chapter 4: Model Capabilities & Limitations**

**Goal:** Classify a list of application error log strings by severity and suggest a likely cause for each, then print a formatted summary table.

**Skills practiced:**
- Sending per-item classification requests
- Prompting for structured output (fixed columns)
- Using `tier="mini"` for a reliable classification task

## Instructions

1. Go to the `start/` directory and open `bug_triager.py`.
2. Read `ERROR_LOGS` and the four severity levels: CRITICAL, HIGH, MEDIUM, LOW.
3. Complete `triage_error()` so it classifies a single log line and returns a dict with keys "severity" and "cause".
4. Complete `print_table()` to render the results as a readable table.
5. Run the file and verify the table makes sense for each log line:
   ```bash
   python exercises/ch04/bug_triager/start/bug_triager.py
   ```
6. Add two of your own log lines to `ERROR_LOGS` and re-run.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
