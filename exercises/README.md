# Exercises

This directory contains the hands-on coding exercises that accompany the book *Building with LLMs: The Developer's Handbook*.

## Exercise Structure

The exercises are organized by chapter (e.g., `ch03`, `ch04`) and capstone projects (`capstone-1`, `capstone-2`). Within each specific exercise directory, you will typically find two folders:

- `start/`: Contains boilerplate code with `TODO` comments. This is where you will write your code.
- `solution/`: Contains the fully working reference implementation. If you get stuck, you can refer to this code.

## Running the Scripts

**Important:** Always execute your scripts from the **root directory** of the repository (i.e. `building-with-llms-companion/`). This ensures that the Python module resolution works properly (so that imports from the `shared` module succeed) and that your `.env` file is located correctly.

Make sure your virtual environment is activated and your `.env` file is properly configured before running the scripts.

**Example: Running a Start Script**
```bash
python exercises/ch03/hello_llm/start/hello_llm.py
```

**Example: Running a Solution Script**
```bash
python exercises/ch03/hello_llm/solution/hello_llm.py
```

You can use this same pattern for all other exercises by replacing the file path with the specific script you want to run. Follow the instructions in the `README.md` file located inside each exercise folder for more specific details about the task.

## Common Code (The `shared` Module)

You will notice that we do not have a `shared` folder duplicated inside the `exercises/` directory. Instead, all common code (such as the `llm_client.py` LiteLLM wrapper) is located in the global `shared/` directory at the root of the repository.

By always running your scripts from the repository root, your code can easily import from this shared module:

```python
from shared.llm_client import LLMClient
```
