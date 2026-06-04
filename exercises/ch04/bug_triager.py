"""
Exercise: Bug Triager
Chapter 4: Model Capabilities & Limitations

Goal: Classify a list of application error log strings by severity and suggest
a likely cause for each, then print a formatted summary table.

Skills practiced:
- Sending per-item classification requests
- Prompting for structured output (fixed columns)
- Using tier="mini" for a reliable classification task

Instructions:
1. Read ERROR_LOGS and the four severity levels: CRITICAL, HIGH, MEDIUM, LOW.
2. Complete triage_error() so it classifies a single log line and returns
   a dict with keys "severity" and "cause".
3. Complete print_table() to render the results as a readable table.
4. Run the file and verify the table makes sense for each log line.
5. Add two of your own log lines to ERROR_LOGS and re-run.

Run: python exercises/ch04/bug_triager.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

ERROR_LOGS = [
    "FATAL: Database connection pool exhausted after 30 retries. Service unavailable.",
    "ERROR: NullPointerException in PaymentService.process() at line 142.",
    "WARNING: Response time exceeded 2000ms for /api/search (avg: 2340ms).",
    "ERROR: Invalid JWT signature. Token rejected for user id=8821.",
    "INFO: Scheduled cache flush completed. 1,204 entries removed.",
    "ERROR: Disk usage at 94% on /dev/sda1. Write operations may fail soon.",
    "WARNING: Retry attempt 2/3 for external shipping API. Timeout after 5s.",
    "CRITICAL: SSL certificate expires in 3 days. Immediate renewal required.",
]

SEVERITY_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def triage_error(log_line: str) -> dict:
    """Classify one log line and return severity + likely cause.

    Args:
        log_line: A single error/warning/info log string.

    Returns:
        A dict with keys:
          "severity" - one of CRITICAL / HIGH / MEDIUM / LOW
          "cause"    - a short (max 10 words) description of the likely cause
    """
    # TODO: Build a messages list where:
    #   - The system message tells the model it is a log analysis assistant
    #     that responds with ONLY two lines:
    #       SEVERITY: <level>
    #       CAUSE: <10 words or fewer>
    #     Valid severity levels: CRITICAL, HIGH, MEDIUM, LOW.
    #   - The user message contains the log_line.
    # Call get_completion with tier="mini" and temperature=0.0.
    # Parse the two lines from the response and return the dict.

    # Hint:
    # messages = [
    #     {"role": "system",
    #      "content": "You are a log analysis assistant. "
    #          "Classify the log line by severity and identify the likely cause. "
    #          "Respond with EXACTLY two lines:\n"
    #          "SEVERITY: CRITICAL | HIGH | MEDIUM | LOW\n"
    #          "CAUSE: <10 words or fewer describing the root cause>"},
    #     {"role": "user", "content": log_line},
    # ]
    # raw = get_completion(messages, tier="mini", temperature=0.0)
    # lines = {l.split(":")[0].strip(): ":".join(l.split(":")[1:]).strip()
    #          for l in raw.strip().splitlines() if ":" in l}
    # return {
    #     "severity": lines.get("SEVERITY", "UNKNOWN"),
    #     "cause": lines.get("CAUSE", "Unknown cause"),
    # }

    raise NotImplementedError("Complete triage_error() to continue.")


def print_table(results: list[dict], logs: list[str]) -> None:
    """Print a formatted table of triage results.

    Args:
        results: List of dicts from triage_error(), one per log line.
        logs: The original log strings in the same order.
    """
    # TODO: Print a table with three columns: SEVERITY, CAUSE, LOG (truncated
    # to 60 characters). Separate header from rows with a line of dashes.
    # Use str.ljust() or f-string width specifiers for alignment.

    # Hint:
    # header = f"{'SEVERITY':<10}  {'CAUSE':<35}  LOG"
    # print(header)
    # print("-" * 90)
    # for r, log in zip(results, logs):
    #     truncated = log[:60] + "..." if len(log) > 60 else log
    #     print(f"{r['severity']:<10}  {r['cause']:<35}  {truncated}")

    raise NotImplementedError("Complete print_table() to continue.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Bug Triager ===\n")
    results = []
    for log in ERROR_LOGS:
        result = triage_error(log)
        results.append(result)
    print_table(results, ERROR_LOGS)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Bug Triager ===
#
# SEVERITY    CAUSE                                LOG
# ------------------------------------------------------------------------------------------
# CRITICAL    Database connection pool exhausted   FATAL: Database connection pool exhausted...
# HIGH        Null pointer in payment processing   ERROR: NullPointerException in PaymentServi...
# MEDIUM      API response latency above threshold WARNING: Response time exceeded 2000ms for...
# HIGH        Invalid authentication token         ERROR: Invalid JWT signature. Token rejected...
# LOW         Routine cache maintenance complete   INFO: Scheduled cache flush completed. 1,20...
# HIGH        Disk near capacity, writes at risk   ERROR: Disk usage at 94% on /dev/sda1. Writ...
# MEDIUM      External API timeout, retrying       WARNING: Retry attempt 2/3 for external shi...
# CRITICAL    SSL certificate expiring imminently  CRITICAL: SSL certificate expires in 3 days...
