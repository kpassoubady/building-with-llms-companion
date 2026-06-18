# Email Drafter Assistant

**Goal:** Build a tool that takes bullet points and returns a professional customer email. Iterate the prompt **3 times** based on observed failures.

**Requirements:**
1. Accept brief bullet points as input.
2. Return: Professional, ready-to-send email.
3. Iterate to fix tone, length, and missing call-to-actions.
4. Follow business email conventions.

## The Iteration Process
1. **v1:** Write your initial prompt. Test with 3 samples. Note failures.
2. **v2:** Fix the most common failure. Test again.
3. **v3:** Fix the next failure. Test again.
4. Document what changed and why at each iteration.

## Instructions

1. Go to the `start/` directory and open `email_drafter.py`.
2. Implement the `draft_email` function using the prompt versions provided.
3. Run the application from your terminal:
   ```bash
   python exercises/ch08/email_drafter/start/email_drafter.py
   ```
4. Observe the differences between the prompt versions across the dataset.

## Getting Stuck?
If you need help or want to see the final working version, check the `solution/` directory.
