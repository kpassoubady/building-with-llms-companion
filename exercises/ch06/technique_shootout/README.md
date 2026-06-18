# Exercise: Technique Shootout

**Chapter 6: Prompting Techniques**

**Goal:** Send the same set of prompts through four different prompting techniques and collect outputs side by side so you can compare quality and style.

**Skills practiced:**
- Zero-shot, few-shot, chain-of-thought (CoT), and role prompting
- Structuring system and user messages for each technique
- Collecting and displaying multi-technique results in a summary table
- Observing when each technique produces notably different answers

## Instructions

1. Go to the `start/` directory and open `technique_shootout.py`.
2. Implement each of the four strategy functions (`zero_shot`, `few_shot`, `chain_of_thought`, `role_prompting`). They share the same signature.
3. Run the file. It will execute `run_shootout()` to run all strategies on every prompt:
   ```bash
   python exercises/ch06/technique_shootout/start/technique_shootout.py
   ```
4. Inspect the printed table - note where outputs diverge across techniques.
5. Add a 5th prompt of your own to `PROMPTS` and re-run.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
