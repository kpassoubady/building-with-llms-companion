# Exercise 1: Fleet Policy RAG System

**Capstone 2: Global Intelligent Fleet Assistant**

Your goal is to build a basic RAG system that answers questions based strictly on the provided Global Fleet Management Driver Policy Guidelines.

## Instructions

1. Open `start/fleet_rag.py`.
2. Load the document `data/global_fleet_policy.md`.
3. Chunk and embed the text using a vector store of your choice (e.g. FAISS, Chroma, or a simple cosine similarity script).
4. Create a prompt that injects the retrieved chunks to accurately answer: *"How often do I need to get an oil change?"*
5. Run the code:
   ```bash
   python exercises/capstone-2/fleet_rag/start/fleet_rag.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
