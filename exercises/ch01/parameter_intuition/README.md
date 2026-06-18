# Exercise: Parameter Intuition

**Chapter 1: Introduction to Generative AI & LLMs**

**Goal:** Compare the mini model (`tier="mini"`) against the default model (`tier="default"`) on the same 5 prompts, then record your observations about quality differences.

**Skills practiced:**
- Calling `get_completion()` with different tier values
- Observing the output quality and verbosity tradeoff between model tiers
- Building intuition for when each tier is appropriate

## Instructions

1. Go to the `start/` directory and open `parameter_intuition.py`.
2. Implement `query_both_tiers()` to send the same prompt to both tiers and return a tuple of `(mini_response, default_response)`.
3. Implement `print_comparison()` to display the two responses side by side.
4. Run the script:
   ```bash
   python exercises/ch01/parameter_intuition/start/parameter_intuition.py
   ```
5. For each prompt, note in the `LOG_NOTES` dict:
   - Which model gave a better answer?
   - Was the quality difference worth the cost increase?

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
