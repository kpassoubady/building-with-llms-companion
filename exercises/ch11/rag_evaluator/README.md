# Exercise: RAG Evaluator

**Chapter 11: Retrieval-Augmented Generation (RAG)**

**Goal:** Run a small evaluation set through the RAG pipeline and compute two metrics: retrieval recall (did the expected source appear in the top-k results?) and answer accuracy (do the answer keywords appear in the generated text?).

**Skills practiced:**
- Systematic RAG evaluation with a labelled eval set
- Retrieval recall: expected_source in top-k sources
- Answer accuracy: checking for expected keyword coverage
- Printing a structured evaluation report

## Instructions

1. Go to the `start/` directory and open `rag_evaluator.py`.
2. Implement `evaluate_retrieval()` to count how many queries surface the expected source in the top-k results.
3. Implement `evaluate_answer()` to run the full RAG query and check how many expected keywords appear in the answer (case-insensitive).
4. Implement `run_evaluation()` to loop over `EVAL_SET`, call both evaluators, and collect per-question results.
5. Run the file and review the printed report. Which questions fail? Why?
   ```bash
   python exercises/ch11/rag_evaluator/start/rag_evaluator.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
