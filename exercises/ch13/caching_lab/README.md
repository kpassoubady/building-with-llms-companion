# Exercise: Caching and Retry Logic

**Chapter 13: Cost, Latency and Error Handling**

**Goal:** Implement a `ResponseCache` backed by a hash of the messages list, and a `completion_with_retry` function with exponential backoff. Demonstrate that repeated identical queries only hit the API once, then print cost savings.

**Skills practiced:**
- Implementing a hash-keyed in-memory cache for LLM responses
- Tracking cache hit/miss statistics
- Exponential backoff retry pattern for `RateLimitError`
- Simulating and handling API failures in tests

## Instructions

1. Go to the `start/` directory and open `caching_lab.py`.
2. Implement `ResponseCache` with `get(messages)` and `set(messages, response)` methods. Use `hashlib.md5` (or `sha256`) over the JSON-serialised messages as the cache key.
3. Implement `completion_with_retry(messages, max_retries=3, base_delay=0.5)` that calls `get_completion` and retries on a `SimulatedRateLimitError` with exponential backoff (`base_delay * 2**attempt`). It must check the cache first and store successful responses.
4. In `main()`, ask `REPEATED_QUESTION` three times using `completion_with_retry`. Only the first call should reach `get_completion`. Print hit/miss stats and an estimate of tokens saved.
5. Demonstrate retry: call `retry_demo()` which raises `SimulatedRateLimitError` on the first two attempts, then succeeds on the third.
6. Run the file:
   ```bash
   python exercises/ch13/caching_lab/start/caching_lab.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
