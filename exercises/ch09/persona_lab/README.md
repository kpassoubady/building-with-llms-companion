# Exercise: Persona Lab

**Chapter 9: Conversation Design & Multi-turn Chat**

**Goal:** Define three distinct personas via system messages, send each the same two questions, and compare how tone, vocabulary, and depth differ.

**Skills practiced:**
- Writing system messages that define persona, scope, and tone
- Observing how system message phrasing shapes model behaviour
- Identifying what to include (and exclude) in a persona definition

## Instructions

1. Go to the `start/` directory and open `persona_lab.py`.
2. Read the three entries in `PERSONAS`. Each has a `name` and a stub `system_content` that you must complete.
3. Complete the `system_content` for all three personas following the guidance in the TODO comments.
4. Complete `ask_persona()` to build the message list and call the model.
5. Run the file and read the contrasting responses side by side:
   ```bash
   python exercises/ch09/persona_lab/start/persona_lab.py
   ```
6. **Optional:** add a fourth persona of your own design.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
