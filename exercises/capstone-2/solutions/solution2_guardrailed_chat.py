import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = "gpt-3.5-turbo"
FAST_MODEL = "gpt-3.5-turbo" # Using same for simplicity

def check_input_guardrail(user_input):
    """
    Uses a fast/cheap LLM call to classify if the user input is about
    automotive services, fleet management, or vehicle repair.
    """
    messages = [
        {"role": "system", "content": "You are a guardrail classifier. Determine if the user's input is related to automotive services, vehicles, fleet management, or driving. Output only 'SAFE' or 'UNSAFE'."},
        {"role": "user", "content": user_input}
    ]
    response = completion(model=FAST_MODEL, messages=messages, temperature=0.0)
    result = response.choices[0].message.content.strip().upper()
    return "SAFE" in result

def check_output_guardrail(bot_response):
    """
    Uses an LLM call to classify if the bot's response contains dangerous
    DIY repair instructions.
    """
    messages = [
        {"role": "system", "content": "You are a safety guardrail. Determine if the following bot response provides dangerous DIY mechanical or electrical repair instructions to a driver. Output only 'SAFE' or 'DANGEROUS'."},
        {"role": "user", "content": bot_response}
    ]
    response = completion(model=FAST_MODEL, messages=messages, temperature=0.0)
    result = response.choices[0].message.content.strip().upper()
    return "SAFE" in result

def generate_response(messages):
    """Calls the LLM with the conversation history."""
    response = completion(model=LLM_MODEL, messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Welcome to the Global Fleet Assistant!")
    print("Type 'exit' to quit.\n")
    
    chat_history = [
        {"role": "system", "content": "You are a helpful automotive fleet assistant. You help drivers diagnose issues, but you MUST NEVER instruct them to perform complex or dangerous repairs themselves (e.g. electrical work, brake replacements). Tell them to visit a certified Global shop."}
    ]
    
    while True:
        user_input = input("Driver: ")
        if user_input.lower() == 'exit':
            break
            
        # 1. Run input guardrail
        if not check_input_guardrail(user_input):
            print("Assistant: I can only help with automotive and fleet-related questions. How can I assist with your vehicle today?")
            continue
        
        # 2. Append user message to history
        chat_history.append({"role": "user", "content": user_input})
        
        # 3. Generate response
        bot_reply = generate_response(chat_history)
        
        # 4. Run output guardrail
        if not check_output_guardrail(bot_reply):
            bot_reply = "I cannot provide specific instructions for that repair as it poses a safety risk. Please take your vehicle to an authorized Global repair center."
        
        print(f"Assistant: {bot_reply}")
        chat_history.append({"role": "assistant", "content": bot_reply})
