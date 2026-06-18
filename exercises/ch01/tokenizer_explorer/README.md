# Exercise: Tokenizer Explorer

**Chapter 1: Introduction to Generative AI & LLMs**

**Goal:** Tokenize 10 sample sentences with `tiktoken` and compare token counts across different input types to build intuition about how LLMs see text.

**Skills practiced:**
- Using `tiktoken` to encode text into tokens
- Observing differences between English, non-English, code, and emoji inputs
- Estimating relative cost across input types

## Instructions

1. Go to the `start/` directory and open `tokenizer_explorer.py`.
2. Run the file as-is to see token counts for the first few sample sentences.
3. Implement `tokenize_and_report()` to encode each sentence and print:
   - the token count
   - the token IDs (first 10, to keep output readable)
   - the cost estimate at GPT-4o input pricing ($2.50 / 1M tokens)
4. Call your function on all 10 `SAMPLE_SENTENCES`.
5. Answer in a comment: which input type uses the most tokens per character?
6. Run the script:
   ```bash
   python exercises/ch01/tokenizer_explorer/start/tokenizer_explorer.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
