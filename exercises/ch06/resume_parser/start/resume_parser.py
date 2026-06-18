import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_RESUME = """
Alex Rivera
alex.rivera@example.com | (555) 234-7890 | linkedin.com/in/alexrivera

SUMMARY
Software engineer with 6 years of experience building backend services and APIs.

SKILLS
Python, Go, PostgreSQL, Redis, Docker, Kubernetes, REST APIs, gRPC

EXPERIENCE
Senior Software Engineer - Acme Corp (2021 - Present)
  - Designed a microservices platform handling 50k requests/second
  - Reduced deployment time by 40% by introducing GitOps workflows

Software Engineer - Startup XYZ (2018 - 2021)
  - Built a real-time notification service in Go serving 1M daily users

EDUCATION
B.S. Computer Science - State University, 2018
"""

EXPECTED_SCHEMA = {
    "name": "string",
    "email": "string",
    "skills": ["list of strings"],
    "years_experience": "integer",
    "last_role": "string",
}


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def extract_resume_data(resume_text):
    """Send the resume to the LLM and return parsed JSON as a Python dict.

    Args:
        resume_text: Plain-text resume string.

    Returns:
        Dict with keys: name, email, skills, years_experience, last_role.
    """
    # TODO: Call get_completion with:
    #   - system: role-prompt as an HR data extraction assistant; instruct it to
    #             return ONLY valid JSON matching the EXPECTED_SCHEMA keys above.
    #             Include the schema in the system message so the model knows
    #             exactly which fields to extract.
    #   - user: the resume_text
    #   - tier="default", temperature=0.0
    # Then parse the returned string with json.loads() and return the dict.
    raise NotImplementedError("Implement extract_resume_data()")


def parse_and_display(data):
    """Print each extracted field in a readable format.

    Args:
        data: Dict returned by extract_resume_data().
    """
    # TODO: Print each field with a label. Format skills as a comma-separated
    #   string. Handle missing keys gracefully using dict.get().
    raise NotImplementedError("Implement parse_and_display()")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 6 - Resume Parser\n")
    print("Extracting data from sample resume...")
    # TODO: update when implemented
    # data = extract_resume_data(SAMPLE_RESUME)
    # print("\nExtracted fields:")
    # print("-" * 40)
    # parse_and_display(data)
    # print("\nRaw JSON returned:")
    # print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
