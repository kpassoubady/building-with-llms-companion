# Exercise: Secure Completion Wrapper

**Chapter 12: Security and Guardrails**

**Goal:** Build a `secure_completion(user_input)` function that layers PII redaction, a sandwich defense system prompt, and a basic output check around `get_completion`.

**Skills practiced:**
- Regex-based PII detection and redaction
- Sandwich defense pattern for prompt injection resistance
- Output filtering to block harmful content leakage
- Composing multiple defense layers into a single wrapper

## Instructions

1. Go to the `start/` directory and open `moderation_layer.py`.
2. Implement `redact_pii(text)` using regex patterns for email, US phone, SSN, and credit card numbers. Replace each match with a placeholder like `[EMAIL]`, `[PHONE]`, `[SSN]`, `[CREDIT_CARD]`.
3. Implement `secure_completion(user_input)` which:
   - Calls `redact_pii` on the user input before sending it to the LLM.
   - Wraps the (redacted) input with a sandwich defense: a system prompt before AND a reminder after the user content.
   - Calls `get_completion` with `tier="mini"`.
   - Runs a basic output check - if the response contains any forbidden phrases, return a safe fallback string instead.
4. Run the wrapper against each entry in `SAMPLE_INPUTS` and print the result.
   ```bash
   python exercises/ch12/moderation_layer/start/moderation_layer.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
