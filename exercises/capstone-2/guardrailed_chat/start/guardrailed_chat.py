import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = "gpt-3.5-turbo"

def check_input_guardrail(user_input):
    """
    Uses a fast/cheap LLM call to classify if the user input is about
    automotive services, fleet management, or vehicle repair.
    Returns True if safe, False if off-topic.
    """
    # TODO: Implement input guardrail
    return True

def check_output_guardrail(bot_response):
    """
    Uses an LLM call to classify if the bot's response contains dangerous
    DIY repair instructions (e.g. bypassing electrical components).
    Returns True if safe, False if dangerous.
    """
    # TODO: Implement output guardrail
    return True

def generate_response(messages):
    """Calls the LLM with the conversation history."""
    response = completion(model=LLM_MODEL, messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Welcome to the Global Fleet Assistant!")
    print("Type 'exit' to quit.\n")
    
    chat_history = [
        {"role": "system", "content": "You are a helpful automotive fleet assistant."}
    ]
    
    while True:
        user_input = input("Driver: ")
        if user_input.lower() == 'exit':
            break
            
        # 1. Run input guardrail
        # TODO: If not safe, print a polite refusal and continue
        
        # 2. Append user message to history
        chat_history.append({"role": "user", "content": user_input})
        
        # 3. Generate response
        # bot_reply = generate_response(chat_history)
        bot_reply = "I'm a placeholder response." # Replace this
        
        # 4. Run output guardrail
        # TODO: If not safe, replace bot_reply with a safe generic message
        
        print(f"Assistant: {bot_reply}")
        chat_history.append({"role": "assistant", "content": bot_reply})
