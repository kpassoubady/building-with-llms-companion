# Exercise: LLM-as-Judge

**Chapter 8: Prompt Iteration & Evaluation**

**Goal:** Implement an LLM-as-judge evaluator that scores a candidate answer 1-5 against a rubric, then run it on three sample answers of varying quality.

**Skills practiced:**
- Designing a rubric-based scoring prompt
- Parsing a structured score from free-form model output
- Using `tier="default"` for quality-sensitive evaluation tasks

## Instructions

1. Go to the `start/` directory and open `llm_judge.py`.
2. Read `RUBRIC` and the three entries in `SAMPLE_ANSWERS`.
3. Complete `build_judge_prompt()` to construct a prompt that asks the model to score the candidate answer 1-5 and give a one-sentence justification.
4. Complete `parse_score()` to extract the integer score from the response.
5. Complete `judge()` to call the model and return `(score, justification)`.
6. Run the file and compare the three scores against your own intuition:
   ```bash
   python exercises/ch08/llm_judge/start/llm_judge.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
