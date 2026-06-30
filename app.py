import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

def main():
    
    client = genai.Client()
    
    prompt = "Explain what an API is in one sentence, then give a real-world analogy."
    
    print("Sending request to Gemini...")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    print("\nAI Response:")
    print(response.text)

if __name__ == "__main__":
    main()