# Exercise: Sentiment Classifier

**Chapter 6: Prompting Techniques**

**Goal:** Classify product reviews as POSITIVE, NEGATIVE, or NEUTRAL using zero-shot prompting, then improve accuracy by adding few-shot examples.

**Skills practiced:**
- Zero-shot classification prompts
- Few-shot prompting with labeled examples
- Comparing prompt strategies on the same inputs
- Structuring system vs user messages

## Instructions

1. Go to the `start/` directory and open `sentiment_classifier.py`.
2. Run `classify_zero_shot()` to see baseline results on all sample reviews.
3. Implement `classify_few_shot()` by adding 3 labeled examples to the prompt.
4. Run the file and run `compare_strategies()` to print side-by-side results and spot differences:
   ```bash
   python exercises/ch06/sentiment_classifier/start/sentiment_classifier.py
   ```
5. Try adding a 4th example that covers a mixed-sentiment edge case.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
