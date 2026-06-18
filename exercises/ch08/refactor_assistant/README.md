# Exercise: Refactor Assistant

**Chapter 8: Prompt Iteration & Evaluation**

**Goal:** Practise the prompt iteration loop by refining a vague refactoring prompt three times, each time fixing a single observed failure.

**Skills practiced:**
- Identifying specific prompt failures and writing targeted fixes
- Comparing v1/v2/v3 outputs to see measurable improvement
- Using `tier="mini"` for rapid iteration

## Instructions

1. Go to the `start/` directory and open `refactor_assistant.py`.
2. Read `INITIAL_PROMPT` and understand why it is too vague.
3. Complete `build_prompt_v2()` by adding the missing constraint (tests).
4. Complete `build_prompt_v3()` by specifying the target language explicitly.
5. Complete `build_prompt_v4()` by adding a length/format constraint.
6. Run the file and read each version's output to observe improvement:
   ```bash
   python exercises/ch08/refactor_assistant/start/refactor_assistant.py
   ```
7. **Optional:** add a v5 that incorporates all your fixes in one prompt.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
