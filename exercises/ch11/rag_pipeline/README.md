# Exercise: RAG Pipeline

**Chapter 11: Retrieval-Augmented Generation (RAG)**

**Goal:** Build a complete end-to-end RAG pipeline that ingests Markdown files from a knowledge base, chunks and embeds them, builds a FAISS index, retrieves the top-k chunks for a query, and generates a cited answer.

**Skills practiced:**
- Ingestion pipeline: load -> chunk -> embed -> store
- Query pipeline: embed query -> FAISS search -> augment prompt -> generate
- Attaching source metadata to chunks for citation
- Grounding the LLM with "Answer ONLY from the provided context"

## Instructions

1. Go to the `start/` directory and open `rag_pipeline.py`.
2. Implement `load_documents()` to read all `.md` files from the knowledge base directory.
3. Implement `chunk_documents()` to split each document and attach source + chunk_id.
4. Implement `embed_chunks()` to embed all chunk texts in a single litellm call.
5. Implement `build_index()` to create a FAISS IndexFlatL2 from the embeddings.
6. Implement `retrieve()` to embed the query and search the index for top-k chunks.
7. Implement `build_rag_prompt()` to format retrieved context with source labels.
8. Run the file and check that the answers reference the correct source files.
   ```bash
   python exercises/ch11/rag_pipeline/start/rag_pipeline.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
