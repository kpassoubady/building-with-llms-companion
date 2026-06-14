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
    messages = [
        {"role": "system", "content": "Extract the grand total cost and a list of services performed from the invoice text. Return valid JSON strictly matching this schema: {\"total\": float, \"services\": [string, string]}"},
        {"role": "user", "content": f"Invoice:\n{invoice_text}"}
    ]
    response = completion(
        model=LLM_MODEL, 
        messages=messages, 
        response_format={"type": "json_object"},
        temperature=0.0
    )
    
    result_str = response.choices[0].message.content
    try:
        return json.loads(result_str)
    except json.JSONDecodeError:
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
        print(f"Text: {item['text']}")
        
        extracted = extract_invoice_data(item['text'])
        print(f"Extracted: {extracted}")
        print(f"Expected : {{'total': {item['expected_total']}, 'services': {item['expected_services']}}}")
        
        # Compare total
        total_match = abs(extracted.get('total', 0.0) - item['expected_total']) < 0.01
        
        # Compare services (rough match checking if lists are same length)
        extracted_services = [s.lower() for s in extracted.get('services', [])]
        expected_services = [s.lower() for s in item['expected_services']]
        
        services_match = len(extracted_services) == len(expected_services)
        
        if total_match and services_match:
            print("✅ PASS")
            correct += 1
        else:
            print("❌ FAIL")
        
    print(f"\nFinal Accuracy: {correct}/{total} ({(correct/total)*100:.1f}%)")

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "invoice_dataset.json")
    if not os.path.exists(data_path):
        data_path = "data/invoice_dataset.json"
        
    dataset = load_dataset(data_path)
    run_evaluation(dataset)
