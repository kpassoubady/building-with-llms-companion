# Exercise: RAG API

**Chapter 11: Retrieval-Augmented Generation (RAG)**

**Goal:** Wrap the RAG pipeline behind a FastAPI application with a POST `/ask` endpoint that accepts a question and returns an answer with source citations.

**Skills practiced:**
- Serving a RAG pipeline as an HTTP API with FastAPI
- Lifespan events for one-time index setup at startup
- Pydantic request/response models
- Connecting the retrieve + generate steps inside an async route handler

## Instructions

1. Go to the `start/` directory and open `rag_api.py`.
2. Implement the startup lifespan function to load, chunk, embed, and index the knowledge base once when the server starts. Store the index and chunks in the app state so the route handler can access them.
3. Implement the `/ask` route handler: call `_retrieve()`, `_build_rag_prompt()`, and `get_completion()` to produce a cited answer.
4. Start the server:
   ```bash
   uvicorn exercises.ch11.rag_api.start.rag_api:app --reload
   ```
5. Test with curl in another terminal:
   ```bash
   curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question": "How do I cancel my subscription?"}'
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
