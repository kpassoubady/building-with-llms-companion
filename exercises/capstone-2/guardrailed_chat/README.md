# Exercise 2: Guardrailed Maintenance Chatbot

**Capstone 2: Global Intelligent Fleet Assistant**

Extend the assistant to handle a multi-turn conversation with a driver experiencing vehicle issues, but ensure the chatbot stays on topic and safe.

## Instructions

1. Open `start/guardrailed_chat.py`.
2. Implement a chat loop that remembers previous turns.
3. Implement an **Input Guardrail** that rejects queries completely unrelated to vehicles or fleet management.
4. Implement an **Output Guardrail** that prevents the bot from providing dangerous DIY repair instructions (e.g., instructing a user how to bypass a battery terminal).
5. Run the code:
   ```bash
   python exercises/capstone-2/guardrailed_chat/start/guardrailed_chat.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
