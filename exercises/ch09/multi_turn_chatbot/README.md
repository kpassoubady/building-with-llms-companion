# Exercise: Multi-Turn Chatbot

**Chapter 9: Conversation Design & Multi-turn Chat**

**Goal:** Build a stateful chat loop that maintains message history so the bot remembers the user's name and preferences across turns.

**Skills practiced:**
- Appending user and assistant messages to a shared history list
- Verifying that context persists across multiple API calls
- Designing a system message that defines persona and scope

## Instructions

1. Go to the `start/` directory and open `multi_turn_chatbot.py`.
2. Complete `add_user_turn()` to append a user message to history.
3. Complete `add_assistant_turn()` to append an assistant message to history.
4. Complete `chat()` to send the full history to the model and record the reply.
5. Run the file, which drives a scripted 5-turn conversation:
   ```bash
   python exercises/ch09/multi_turn_chatbot/start/multi_turn_chatbot.py
   ```
6. Observe that turn 4 ("What's my name?") is answered correctly because the history carries context from turn 1.
7. **Optional:** replace the scripted loop with `input()` for a live session.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
