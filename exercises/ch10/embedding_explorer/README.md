# Exercise: Embedding Explorer

**Chapter 10: Embeddings & Vector Databases**

**Goal:** Embed 20 sentences covering different topics, build a full cosine-similarity matrix with numpy, and surface the most similar sentence pairs and natural clusters.

**Skills practiced:**
- Calling `litellm.embedding()` for batch embedding
- Computing pairwise cosine similarity with numpy
- Reading a similarity matrix to identify clusters
- Interpreting scores: 0.90+ very similar, 0.70-0.89 related, below 0.50 unrelated

## Instructions

1. Go to the `start/` directory and open `embedding_explorer.py`.
2. Run `embed_sentences()` to get vectors for all `SENTENCES`.
3. Implement `cosine_similarity_matrix()` to return an NxN numpy array of pairwise scores.
4. Implement `find_top_pairs()` to scan the upper triangle and return the highest-scoring pairs.
5. Run the file and look at the printed pairs - do the clusters match your intuition?
   ```bash
   python exercises/ch10/embedding_explorer/start/embedding_explorer.py
   ```
6. **Bonus:** add 2 more sentences on a new topic and re-run to see where they land.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
