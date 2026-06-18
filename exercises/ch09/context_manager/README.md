# Exercise: Context Manager

**Chapter 9: Conversation Design & Multi-turn Chat**

**Goal:** Implement three context strategies (full history, sliding window, running summary) and compare their approximate token cost over a 10-turn conversation.

**Skills practiced:**
- Truncating and windowing message history
- Requesting running summaries to compress old context
- Reading `response.usage.prompt_tokens` to measure real token cost

## Instructions

1. Go to the `start/` directory and open `context_manager.py`.
2. Read `CONVERSATION` - a pre-built 10-turn history used as input.
3. Complete `apply_full_history()` - returns the list unchanged.
4. Complete `apply_sliding_window()` - keeps system message plus last N turns.
5. Complete `apply_summary_strategy()` - calls the model to summarise old turns, then returns `[system, summary_message] + last N turns verbatim`.
6. Complete `measure_tokens()` - sends the trimmed history to the model, reads `response.usage.prompt_tokens`, and returns the count.
7. Run the file and compare the three token counts:
   ```bash
   python exercises/ch09/context_manager/start/context_manager.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
