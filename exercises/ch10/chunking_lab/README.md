# Exercise: Chunking Lab

**Chapter 10: Embeddings & Vector Databases**

**Goal:** Chunk a sample markdown document three ways, embed every chunk and a query, then compare which strategy surfaces the most relevant chunk.

**Skills practiced:**
- Fixed-size chunking by character count
- Paragraph-boundary chunking (semantic split)
- Overlap chunking (fixed-size with shared context at boundaries)
- Embedding chunks and a query with `litellm`
- Scoring relevance by cosine similarity

## Instructions

1. Go to the `start/` directory and open `chunking_lab.py`.
2. Implement `chunk_fixed()` to split `DOCUMENT` by `chunk_size` characters (no overlap).
3. Implement `chunk_by_paragraph()` to split on blank lines, skipping empty strings.
4. Implement `chunk_with_overlap()` to split by `chunk_size` with an overlap step.
5. Implement `embed_and_rank()` to embed all chunks + the query, then return chunks sorted by cosine similarity to the query vector.
6. Run the file - which strategy returns the most relevant top chunk for `QUERY`?
   ```bash
   python exercises/ch10/chunking_lab/start/chunking_lab.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
