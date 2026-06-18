import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
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
    """Classify one log line and return severity + likely cause."""
    messages = [
        {"role": "system",
         "content": "You are a log analysis assistant. "
             "Classify the log line by severity and identify the likely cause. "
             "Respond with EXACTLY two lines:\n"
             "SEVERITY: CRITICAL | HIGH | MEDIUM | LOW\n"
             "CAUSE: <10 words or fewer describing the root cause>"},
        {"role": "user", "content": log_line},
    ]
    raw = get_completion(messages, tier="mini", temperature=0.0)
    lines = {l.split(":")[0].strip(): ":".join(l.split(":")[1:]).strip()
             for l in raw.strip().splitlines() if ":" in l}
    return {
        "severity": lines.get("SEVERITY", "UNKNOWN"),
        "cause": lines.get("CAUSE", "Unknown cause"),
    }


def print_table(results: list[dict], logs: list[str]) -> None:
    """Print a formatted table of triage results."""
    header = f"{'SEVERITY':<10}  {'CAUSE':<35}  LOG"
    print(header)
    print("-" * 90)
    for r, log in zip(results, logs):
        truncated = log[:60] + "..." if len(log) > 60 else log
        print(f"{r['severity']:<10}  {r['cause']:<35}  {truncated}")


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
