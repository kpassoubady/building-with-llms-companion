# Exercise 3: Maintenance Invoice Evaluator

**Capstone 2: Global Intelligent Fleet Assistant**

You have been tasked with automating invoice data extraction. To ensure the LLM is accurate before deploying to production, you need to build an evaluation harness.

## Instructions

1. Open `start/invoice_eval.py`.
2. The dataset `data/invoice_dataset.json` is loaded for you.
3. Write an LLM prompt that extracts the total cost and list of services from the messy invoice text.
4. Compare the LLM's output against the `expected_total` and `expected_services` in the dataset.
5. Calculate and print a final accuracy score (e.g., "4/5 invoices correctly parsed").
6. Run the code:
   ```bash
   python exercises/capstone-2/invoice_eval/start/invoice_eval.py
   ```

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
