"""
Exercise: Tokenizer Explorer
Chapter 1: Introduction to Generative AI & LLMs

Goal: Tokenize 10 sample sentences with tiktoken and compare token counts
across different input types to build intuition about how LLMs see text.

Skills practiced:
- Using tiktoken to encode text into tokens
- Observing differences between English, non-English, code, and emoji inputs
- Estimating relative cost across input types

Instructions:
1. Run the file as-is to see token counts for the first few sample sentences.
2. Implement `tokenize_and_report()` to encode each sentence and print:
   - the token count
   - the token IDs (first 10, to keep output readable)
   - the cost estimate at GPT-4o input pricing ($2.50 / 1M tokens)
3. Call your function on all 10 SAMPLE_SENTENCES.
4. Answer in a comment: which input type uses the most tokens per character?

Run: python exercises/ch01/tokenizer_explorer.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import tiktoken

# 10 sample sentences covering different input categories
SAMPLE_SENTENCES = [
    # English - short
    "Hello, world!",
    # English - long
    "You are a senior software engineer. Review this pull request and list all bugs, style issues, and security concerns. Be thorough.",
    # French
    "Bonjour, comment allez-vous aujourd'hui?",
    # Tamil
    "நீங்கள் எப்படி இருக்கிறீர்கள்?",
    # Japanese
    "今日はいい天気ですね。",
    # Python code
    "def fibonacci(n):\n    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
    # JSON-like structured text
    '{"name": "Alice", "role": "engineer", "active": true}',
    # Emojis only
    "🚀🤖✨🔥💡",
    # Mixed English + emoji
    "Ship it! 🚀 The tests pass. 🟢",
    # URL / technical noise
    "https://api.openai.com/v1/chat/completions?model=gpt-4o&stream=true",
]

GPT4O_INPUT_PRICE_PER_MILLION = 2.50  # USD per 1M tokens


def tokenize_and_report(sentence: str, enc: tiktoken.Encoding) -> int:
    """Encode `sentence`, print token stats, and return the token count.

    TODO: Implement this function.
      1. Encode the sentence with enc.encode(sentence).
      2. Calculate the cost using GPT4O_INPUT_PRICE_PER_MILLION.
      3. Print: token count, first 10 token IDs, cost, and a truncated preview.
      4. Return the token count.

    # Hint:
    # tokens = enc.encode(sentence)
    # cost = len(tokens) * GPT4O_INPUT_PRICE_PER_MILLION / 1_000_000
    # preview = (sentence[:60] + "...") if len(sentence) > 60 else sentence
    # print(f"  {len(tokens):4} tokens | ${cost:.6f} | ids={tokens[:10]} | {repr(preview)}")
    # return len(tokens)
    """
    raise NotImplementedError("Implement tokenize_and_report()")


def main():
    enc = tiktoken.get_encoding("cl100k_base")  # used by gpt-4o and gpt-4o-mini

    print("Tokenizer Explorer - tiktoken (cl100k_base / GPT-4o)")
    print("=" * 60)

    counts = []
    for i, sentence in enumerate(SAMPLE_SENTENCES, 1):
        print(f"\n[{i:02}] Input:")
        # TODO: call tokenize_and_report(sentence, enc) and append the result to counts
        # counts.append(tokenize_and_report(sentence, enc))

    # TODO: Uncomment and complete the summary once tokenize_and_report is implemented.
    # print("\n" + "=" * 60)
    # print("Summary")
    # print(f"  Total tokens across all inputs: {sum(counts)}")
    # max_idx = counts.index(max(counts))
    # print(f"  Most expensive input (#{max_idx + 1}): {max(counts)} tokens")
    # chars = [len(s) for s in SAMPLE_SENTENCES]
    # ratios = [c / ch for c, ch in zip(counts, chars)]
    # max_ratio_idx = ratios.index(max(ratios))
    # print(f"  Highest tokens-per-char (#{max_ratio_idx + 1}): {max(ratios):.2f}")


if __name__ == "__main__":
    main()


# Expected output (illustrative):
#
# Tokenizer Explorer - tiktoken (cl100k_base / GPT-4o)
# ============================================================
#
# [01] Input:
#    3 tokens | $0.000008 | ids=[9906, 11, 1917] | 'Hello, world!'
#
# [02] Input:
#   30 tokens | $0.000075 | ids=[2675, 527, 264, 8792, 4382, ...] | 'You are a senior software engineer. Review thi...'
#
# [04] Input:  (Tamil)
#   12 tokens | $0.000030 | ids=[...] | 'நீங்கள் எப்படி இருக்கிறீர்கள்?'
#   (more tokens per character than English - non-Latin scripts use more tokens)
#
# [08] Input:  (Emojis)
#    5 tokens | $0.000013 | ids=[...] | ':rocket::robot::sparkles::fire::bulb:'
#
# Summary
#   Total tokens across all inputs: ~150
#   Most expensive input (#2): 30 tokens
#   Highest tokens-per-char (#4 or #5): non-English script
