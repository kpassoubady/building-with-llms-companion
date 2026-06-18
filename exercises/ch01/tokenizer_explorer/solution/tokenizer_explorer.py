import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

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
    """Encode `sentence`, print token stats, and return the token count."""
    tokens = enc.encode(sentence)
    cost = len(tokens) * GPT4O_INPUT_PRICE_PER_MILLION / 1_000_000
    preview = (sentence[:60] + "...") if len(sentence) > 60 else sentence
    print(f"  {len(tokens):4} tokens | ${cost:.6f} | ids={tokens[:10]} | {repr(preview)}")
    return len(tokens)


def main():
    enc = tiktoken.get_encoding("cl100k_base")  # used by gpt-4o and gpt-4o-mini

    print("Tokenizer Explorer - tiktoken (cl100k_base / GPT-4o)")
    print("=" * 60)

    counts = []
    for i, sentence in enumerate(SAMPLE_SENTENCES, 1):
        print(f"\n[{i:02}] Input:")
        counts.append(tokenize_and_report(sentence, enc))

    print("\n" + "=" * 60)
    print("Summary")
    print(f"  Total tokens across all inputs: {sum(counts)}")
    max_idx = counts.index(max(counts))
    print(f"  Most expensive input (#{max_idx + 1}): {max(counts)} tokens")
    chars = [len(s) for s in SAMPLE_SENTENCES]
    ratios = [c / ch for c, ch in zip(counts, chars)]
    max_ratio_idx = ratios.index(max(ratios))
    print(f"  Highest tokens-per-char (#{max_ratio_idx + 1}): {max(ratios):.2f}")


if __name__ == "__main__":
    main()
