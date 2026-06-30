import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def explain_code(code_snippet, mode="explain"):
    """
    Analyzes code snippets to either explain their functionality or debug errors.
    """
    client = genai.Client()
    
    if mode == "explain":
        system_instruction = "You are an elite software engineering instructor. Walk through the provided code step-by-step and explain its purpose cleanly and intuitively."
    elif mode == "debug":
        system_instruction = "You are a senior debugging assistant. Review the provided code snippet, find any syntax or logical bugs, explain why they occur, and provide the corrected version."
    else:
        system_instruction = "Analyze the following code snippet and provide actionable insights."

    prompt = f"""
    Context: {system_instruction}
    
    Code Snippet to analyze:
    ```python
    {code_snippet}
    ```
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text


if __name__ == "__main__":
    broken_code = """
def calculate_average(numbers)
total = sum(numbers)
    return total / len(numbers)
    """
    
    print("--- TESTING MODE: EXPLAIN ---")
    explanation = explain_code(broken_code, mode="explain")
    print(explanation)
    
    print("\n" + "="*40 + "\n")
    
    print("--- TESTING MODE: DEBUG ---")
    debugging_results = explain_code(broken_code, mode="debug")
    print(debugging_results)