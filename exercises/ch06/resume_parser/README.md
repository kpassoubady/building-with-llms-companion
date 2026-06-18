# Exercise: Resume Parser

**Chapter 6: Prompting Techniques**

**Goal:** Extract structured data from a plain-text resume using a JSON output prompt, then parse and display each field cleanly.

**Skills practiced:**
- Structured output prompting (JSON schema in prompt)
- Parsing and validating model-returned JSON
- Role prompting (HR data-extraction assistant)
- Handling optional or missing fields gracefully

## Instructions

1. Go to the `start/` directory and open `resume_parser.py`.
2. Implement `extract_resume_data()` to prompt the model for JSON output.
3. Implement `parse_and_display()` to parse the JSON and print each field.
4. Run the file and verify the extracted fields match the sample resume:
   ```bash
   python exercises/ch06/resume_parser/start/resume_parser.py
   ```
5. Try replacing `SAMPLE_RESUME` with your own resume text and re-run.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
