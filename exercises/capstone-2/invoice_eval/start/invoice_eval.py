import json
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = "gpt-3.5-turbo"

def load_dataset(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_invoice_data(invoice_text):
    """
    Uses the LLM to extract 'total' (float) and 'services' (list of strings).
    Forces JSON output.
    """
    # TODO: Write a prompt asking for JSON with 'total' and 'services' keys
    # TODO: Call litellm with response_format={ "type": "json_object" }
    # TODO: Parse and return the JSON
    return {"total": 0.0, "services": []}

def run_evaluation(dataset):
    """
    Iterates over the dataset, calls the extractor, and compares the result 
    against the expected values.
    """
    correct = 0
    total = len(dataset)
    
    for item in dataset:
        print(f"\nEvaluating Invoice {item['id']}...")
        # TODO: Extract data
        
        # TODO: Compare extracted total vs expected_total
        # TODO: Compare extracted services vs expected_services
        
        # TODO: If both match (or are close enough), increment 'correct'
        
    print(f"\nFinal Accuracy: {correct}/{total} ({(correct/total)*100:.1f}%)")

if __name__ == "__main__":
    dataset = load_dataset(os.path.join(os.path.dirname(__file__), "..", "..", "data", "invoice_dataset.json"))
    # run_evaluation(dataset)
    print("Implement the TODOs to run the evaluation.")
