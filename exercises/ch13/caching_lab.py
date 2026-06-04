"""
Exercise: Caching and Retry Logic
Chapter 13: Cost, Latency and Error Handling

Goal: Implement a ResponseCache backed by a hash of the messages list,
and a completion_with_retry function with exponential backoff. Demonstrate
that repeated identical queries only hit the API once, then print cost savings.

Skills practiced:
- Implementing a hash-keyed in-memory cache for LLM responses
- Tracking cache hit/miss statistics
- Exponential backoff retry pattern for RateLimitError
- Simulating and handling API failures in tests

Instructions:
1. Implement ResponseCache with get(messages) and set(messages, response)
   methods. Use hashlib.md5 (or sha256) over the JSON-serialised messages
   as the cache key.
2. Implement completion_with_retry(messages, max_retries=3, base_delay=0.5)
   that calls get_completion and retries on a SimulatedRateLimitError with
   exponential backoff (base_delay * 2**attempt). It must check the cache
   first and store successful responses.
3. In main(), ask REPEATED_QUESTION three times using completion_with_retry.
   Only the first call should reach get_completion. Print hit/miss stats
   and an estimate of tokens saved.
4. Demonstrate retry: call retry_demo() which raises SimulatedRateLimitError
   on the first two attempts, then succeeds on the third.

Run: python exercises/ch13/caching_lab.py  (from the repo root)
"""

import os
import sys
import json
import time
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
REPEATED_QUESTION = [{"role": "user", "content": "What is the difference between a list and a tuple in Python?"}]

# Rough cost estimate used for the savings display (dollars per 1K tokens)
MINI_COST_PER_1K_TOKENS = 0.00015
ESTIMATED_TOKENS_PER_RESPONSE = 120


# ---------------------------------------------------------------------------
# Simulated exception - stands in for litellm.exceptions.RateLimitError
# ---------------------------------------------------------------------------
class SimulatedRateLimitError(Exception):
    """Raised in tests to simulate an API rate limit (HTTP 429)."""


# ---------------------------------------------------------------------------
# Step 1: Response cache
# ---------------------------------------------------------------------------
class ResponseCache:
    """In-memory cache keyed by a hash of the messages list.

    Attributes:
        hits: Number of times a cached value was returned.
        misses: Number of times the cache had no entry.
    """

    def __init__(self):
        self._store = {}
        self.hits = 0
        self.misses = 0

    def _key(self, messages):
        """Return a stable hex digest for a messages list.

        Hint: json.dumps(messages, sort_keys=True).encode() then hashlib.md5(...).hexdigest()
        """
        # TODO: Implement cache key generation.
        raise NotImplementedError("Implement _key")

    def get(self, messages):
        """Return cached response or None; update hit/miss counters.

        Hint:
        #   key = self._key(messages)
        #   if key in self._store:
        #       self.hits += 1
        #       return self._store[key]
        #   self.misses += 1
        #   return None
        """
        # TODO: Implement cache lookup.
        raise NotImplementedError("Implement get")

    def set(self, messages, response):
        """Store response under the key derived from messages.

        Hint:
        #   self._store[self._key(messages)] = response
        """
        # TODO: Implement cache store.
        raise NotImplementedError("Implement set")

    def stats(self):
        total = self.hits + self.misses
        rate = (self.hits / total * 100) if total else 0
        return {"hits": self.hits, "misses": self.misses, "hit_rate_pct": round(rate, 1)}


# ---------------------------------------------------------------------------
# Step 2: Retry wrapper
# ---------------------------------------------------------------------------
_cache = ResponseCache()


def completion_with_retry(messages, max_retries=3, base_delay=0.5):
    """Return a completion, using the cache and retrying on rate limit errors.

    Check the cache first. On a miss, call get_completion. If SimulatedRateLimitError
    is raised, wait base_delay * (2 ** attempt) seconds and retry up to max_retries times.
    Store successful responses in the cache before returning.

    Args:
        messages: List of message dicts.
        max_retries: Maximum retry attempts after a rate limit error.
        base_delay: Base wait time in seconds (doubles each retry).

    Returns:
        Response string.

    Raises:
        SimulatedRateLimitError: If all retries are exhausted.

    Hint:
    #   cached = _cache.get(messages)
    #   if cached:
    #       return cached
    #   for attempt in range(max_retries + 1):
    #       try:
    #           response = get_completion(messages, tier="mini")
    #           _cache.set(messages, response)
    #           return response
    #       except SimulatedRateLimitError:
    #           if attempt == max_retries:
    #               raise
    #           wait = base_delay * (2 ** attempt)
    #           print(f"  Rate limit hit - waiting {wait:.1f}s (attempt {attempt + 1})")
    #           time.sleep(wait)
    """
    # TODO: Implement completion_with_retry.
    raise NotImplementedError("Implement completion_with_retry")


# ---------------------------------------------------------------------------
# Step 3: Retry demo using a patched version that fails first
# ---------------------------------------------------------------------------
def retry_demo():
    """Show exponential backoff: fail twice, then succeed on the third try."""
    attempt_counter = {"n": 0}
    original_get = get_completion

    def flaky_get(messages, **kwargs):
        attempt_counter["n"] += 1
        if attempt_counter["n"] <= 2:
            raise SimulatedRateLimitError("Simulated 429 - rate limit exceeded")
        return original_get(messages, **kwargs)

    # TODO: Monkey-patch get_completion inside the caching_lab module,
    # call completion_with_retry with a demo question, then restore the original.
    #
    # Hint:
    #   import caching_lab  (already self, use module-level name)
    #   You can swap the reference in the global namespace:
    #
    #   import exercises.ch13.caching_lab as this_module  -- not needed; use globals()
    #
    # Simpler approach - pass flaky_get as a callable and call directly:
    #   demo_messages = [{"role": "user", "content": "Name one benefit of caching."}]
    #   attempt_counter = {"n": 0}
    #   for attempt in range(4):
    #       try:
    #           attempt_counter["n"] += 1
    #           if attempt_counter["n"] <= 2:
    #               raise SimulatedRateLimitError("Simulated 429")
    #           response = get_completion(demo_messages, tier="mini")
    #           print(f"  Retry demo succeeded on attempt {attempt + 1}: {response[:60]}...")
    #           break
    #       except SimulatedRateLimitError as e:
    #           wait = 0.5 * (2 ** attempt)
    #           print(f"  Attempt {attempt + 1} failed ({e}) - retrying in {wait:.1f}s")
    #           time.sleep(wait)
    raise NotImplementedError("Implement retry_demo")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=== Caching Lab ===\n")

    # Ask the same question three times
    print("Asking the same question 3 times...\n")
    for i in range(3):
        response = completion_with_retry(REPEATED_QUESTION)
        label = "API call" if (i == 0) else "cached"
        print(f"  Call {i + 1} ({label}): {response[:70]}...\n")

    stats = _cache.stats()
    print(f"Cache stats: {stats}")
    tokens_saved = stats["hits"] * ESTIMATED_TOKENS_PER_RESPONSE
    cost_saved = tokens_saved / 1000 * MINI_COST_PER_1K_TOKENS
    print(f"Estimated tokens saved: {tokens_saved}")
    print(f"Estimated cost saved:   ${cost_saved:.6f}\n")

    print("--- Retry demo ---")
    retry_demo()


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Caching Lab ===
#
# Asking the same question 3 times...
#
#   Call 1 (API call): A list is mutable while a tuple is immutable...
#   Call 2 (cached):   A list is mutable while a tuple is immutable...
#   Call 3 (cached):   A list is mutable while a tuple is immutable...
#
# Cache stats: {'hits': 2, 'misses': 1, 'hit_rate_pct': 66.7}
# Estimated tokens saved: 240
# Estimated cost saved:   $0.000036
#
# --- Retry demo ---
#   Attempt 1 failed (Simulated 429 - rate limit exceeded) - retrying in 0.5s
#   Attempt 2 failed (Simulated 429 - rate limit exceeded) - retrying in 1.0s
#   Retry demo succeeded on attempt 3: Caching reduces API calls and cost...
