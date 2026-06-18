# Exercise: Hello LLM

**Chapter 3: Working with LLM APIs**

**Goal:** Make 5 `get_completion` calls covering 5 different NLP tasks and print each result, gaining confidence with the message format and API flow.

**Skills practiced:**
- Constructing messages lists with "user" and "system" roles
- Calling `get_completion()` for varied NLP tasks
- Interpreting and printing model responses

## Instructions

1. Go to the `start/` directory and open `hello_llm.py`.
2. Implement each of the 5 task functions below (one per NLP task).
3. Each function must build a messages list and call `get_completion()`.
4. Run the file - you should see 5 labeled outputs.
   ```bash
   python exercises/ch03/hello_llm/start/hello_llm.py
   ```
5. Experiment: swap `tier="mini"` for `tier="default"` on the quality-sensitive tasks and compare the output.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
