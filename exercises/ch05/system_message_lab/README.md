# Exercise: System Message Lab

**Chapter 5: Prompt Engineering Fundamentals**

**Goal:** Send the same user message with 5 different system messages and observe how dramatically the system message changes the tone, structure, and depth of the response.

**Skills practiced:**
- Understanding the system message as a persistent persona and rule layer
- Seeing the effect of role, tone, and format constraints on output
- Designing system messages for different audiences and use cases

## Instructions

1. Go to the `start/` directory and open `system_message_lab.py`.
2. Read `USER_MESSAGE` - this never changes across the 5 calls.
3. Read `SYSTEM_MESSAGES` - each entry defines a different persona/constraint.
4. Complete `call_with_system()` to send the combined system+user message.
5. Run the file and compare the 5 responses printed in order:
   ```bash
   python exercises/ch05/system_message_lab/start/system_message_lab.py
   ```
6. Write a 6th system message of your own (e.g. "sarcastic critic" or "haiku poet") and add it to `SYSTEM_MESSAGES`.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
