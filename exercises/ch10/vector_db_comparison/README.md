# Exercise: Vector DB Comparison

**Chapter 10: Embeddings & Vector Databases**

**Goal:** Load the same 5 documents into both FAISS (with a parallel metadata list) and Chroma (built-in metadata), run the same query against each, and compare the API style, returned text, and metadata handling.

**Skills practiced:**
- Building a FAISS IndexFlatL2 and pairing it with a metadata list
- Creating a Chroma collection with documents and metadata
- Running semantic search with both databases
- Recognising the trade-offs: FAISS is a raw index, Chroma manages metadata for you

## Instructions

1. Go to the `start/` directory and open `vector_db_comparison.py`.
2. Implement `build_faiss_index()` to embed `DOCUMENTS` and add vectors to a FAISS index.
3. Implement `search_faiss()` to embed the query and call `index.search()`.
4. Implement `build_chroma_collection()` to add `DOCUMENTS` to a Chroma collection.
5. Implement `search_chroma()` to call `collection.query()` and format the results.
6. Run the file - do both databases return the same top document?
   ```bash
   python exercises/ch10/vector_db_comparison/start/vector_db_comparison.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
