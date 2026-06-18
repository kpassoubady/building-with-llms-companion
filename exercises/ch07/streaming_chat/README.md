# Exercise: Streaming Chat

**Chapter 7: API Parameters & Output Control**

**Goal:** Build a terminal chat loop that prints tokens as they arrive using litellm streaming, and maintains conversation history across turns.

**Skills practiced:**
- Using `litellm.completion(..., stream=True)` for token-by-token output
- Maintaining a growing messages list for multi-turn context
- Detecting and handling stream end and error conditions
- Graceful exit on 'quit' or 'exit' command

## Instructions

1. Go to the `start/` directory and open `streaming_chat.py`.
2. Implement `stream_response()` to iterate chunks and print tokens as they arrive.
3. Implement `chat_loop()` to manage history and call `stream_response()` per turn.
4. Run the file, type a message, and watch tokens stream in real time:
   ```bash
   python exercises/ch07/streaming_chat/start/streaming_chat.py
   ```
5. Type 'quit' to exit. Notice how the assistant remembers earlier turns.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
