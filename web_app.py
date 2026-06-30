import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

# Load your local .env configuration
load_dotenv()

# Set up the Page configuration for the UI layout
st.set_page_config(
    page_title="Gemini Code Assistant", 
    page_icon="💻", 
    layout="centered"
)

def explain_code(code_snippet, mode="explain"):
    """Core logic hitting the Gemini SDK"""
    # Initialize Client (automatically uses GEMINI_API_KEY from .env)
    client = genai.Client()
    
    # Context-driven prompt configurations
    if mode == "explain":
        system_instruction = "You are an elite software engineering instructor. Walk through the provided code step-by-step and explain its purpose cleanly and intuitively."
    elif mode == "debug":
        system_instruction = "You are a senior debugging assistant. Review the provided code snippet, find any syntax or logical bugs, explain why they occur, and provide the corrected version clearly inside markdown code blocks."
    else:
        system_instruction = "Analyze the code snippet and provide actionable insights."

    prompt = f"""
    Context: {system_instruction}
    
    Code Snippet to analyze:
    ```
    {code_snippet}
    ```
    """
    
    # Generate content using a stable model route
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text


# --- USER INTERFACE (UI) ---
st.title("💻 Gemini Code Explainer & Debugger")
st.write("Paste your raw code snippet below and select whether you want a walkthrough explanation or bug fixes.")

# 1. Selection option for the application mode
mode_selection = st.radio(
    "Choose Mode:",
    options=["Explain Functionality", "Identify & Fix Bugs"],
    index=0,
    horizontal=True
)

# Map the radio button text to the internal function parameters
selected_mode = "explain" if mode_selection == "Explain Functionality" else "debug"

# 2. Raw Text/Code input text area component
code_input = st.text_area(
    "Paste Code Here:", 
    placeholder="def mystery_func(x):\n    return [i for i in x if i % 2 == 0]", 
    height=200
)

# 3. Execution Action trigger button
if st.button("Analyze Code", type="primary"):
    if not code_input.strip():
        st.warning("Please enter some code before analyzing!")
    else:
        # Show an elegant loading spinner while the API works
        with st.spinner("Processing with Gemini..."):
            try:
                # Fire backend request
                analysis_result = explain_code(code_input, mode=selected_mode)
                
                # Render markdown back onto the UI
                st.success("Analysis Complete!")
                st.markdown("### Output Analysis")
                st.markdown(analysis_result)
                
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")