# Exercise: Temperature Lab

**Chapter 7: API Parameters & Output Control**

**Goal:** Generate marketing taglines for a product at five different temperature settings and observe how diversity and determinism change with each value.

**Skills practiced:**
- Passing temperature to get_completion
- Using `get_completion_full` to inspect finish_reason
- Observing determinism (low temp) vs creativity (high temp)
- Formatting and comparing multi-run outputs

## Instructions

1. Go to the `start/` directory and open `temperature_lab.py`.
2. Implement `generate_taglines()` to call the API at a given temperature.
3. Run the file, which executes `run_temperature_sweep()` to generate taglines at all five temperatures:
   ```bash
   python exercises/ch07/temperature_lab/start/temperature_lab.py
   ```
4. Note which temperatures produce repetitive vs wildly varied outputs.
5. Try running the sweep twice and compare - which temperatures are stable?

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
