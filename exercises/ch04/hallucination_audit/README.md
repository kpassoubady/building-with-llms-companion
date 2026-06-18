# Exercise: Hallucination Audit

**Chapter 4: Model Capabilities & Limitations**

**Goal:** Ask the model 10 factual questions with known correct answers, check each response against the expected answer, and report an accuracy score. Demonstrates why fact-critical outputs require external verification.

**Skills practiced:**
- Identifying hallucination-prone question types
- Programmatic answer validation (substring / keyword matching)
- Interpreting accuracy results as a capability signal

## Instructions

1. Go to the `start/` directory and open `hallucination_audit.py`.
2. Read `QUESTIONS_AND_ANSWERS`. Each entry has "question", "expected_keywords", and a "note" explaining why it is tricky for LLMs.
3. Complete `ask_question()` to send one question and return the model's answer.
4. Complete `check_answer()` to return True when ALL expected_keywords appear (case-insensitive) in the model's answer.
5. Run the file. Note which categories the model gets wrong most often:
   ```bash
   python exercises/ch04/hallucination_audit/start/hallucination_audit.py
   ```
6. Add two questions of your own (one easy, one hard) and re-run.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
