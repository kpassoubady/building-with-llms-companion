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
