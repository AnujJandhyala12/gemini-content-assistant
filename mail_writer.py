import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def write_email(purpose, recipient, tone, key_points, sender_name):
    """
    Generates a professional email based on structured user inputs.
    """
    client = genai.Client()
    
    formatted_points = "\n".join([f"- {point}" for point in key_points])
    
    prompt = f"""
    You are an expert executive assistant. Write a complete, ready-to-send email based on the following specific constraints:
    
    - **Recipient**: {recipient}
    - **Sender**: {sender_name}
    - **Purpose**: {purpose}
    - **Tone**: {tone}
    - **Key Points to Include**:
    {formatted_points}
    
    Requirements:
    1. Provide a professional and context-appropriate salutation/greeting.
    2. Write the body ensuring all key points are fully integrated naturally.
    3. Conclude with an appropriate closing and a placeholder for the sender's name.
    4. Return ONLY the final email text. Do not include any intro, outro, conversational commentary, or markdown formatting blocks (like ```).
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    
    return response.text

if __name__ == "__main__":
    email = write_email(
        purpose="request sick leave",
        recipient="manager",
        tone="formal",
        key_points=[
            "Feeling unwell since morning", 
            "Will be unavailable today", 
            "Will catch up on work tomorrow"
        ],
        sender_name="Anuj Jandhyala"
    )
    print(email)