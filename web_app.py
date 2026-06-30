import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

# Load environment variables
load_dotenv()

# Set up the Page layout
st.set_page_config(
    page_title="Gemini AI Multi-Tool", 
    page_icon="🤖", 
    layout="centered"
)

# ---------------------------------------------------------
# CORE BACKEND FUNCTIONS
# ---------------------------------------------------------

def basic_chat(prompt_text):
    """Feature 1: Basic Chat interaction"""
    client = genai.Client()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_text
    )
    return response.text


def write_email(purpose, recipient, tone, key_points, sender_name):
    """Feature 2: Smart Email Writer with structured inputs"""
    client = genai.Client()
    formatted_points = "\n".join([f"- {point}" for point in key_points])
    
    prompt = f"""
    You are an expert executive assistant. Write a complete, ready-to-send email based on the following constraints:
    - **Recipient**: {recipient}
    - **Sender**: {sender_name}
    - **Purpose**: {purpose}
    - **Tone**: {tone}
    - **Key Points to Include**:
    {formatted_points}
    
    Requirements:
    1. Provide an appropriate salutation/greeting addressed to {recipient}.
    2. Sign off cleanly using the sender's name: {sender_name}.
    3. Return ONLY the final email text. Omit any markdown code block wrappers (```).
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text


def explain_code(code_snippet, mode="explain"):
    """Feature 3: Code Explainer & Debugger"""
    client = genai.Client()
    
    if mode == "explain":
        system_instruction = "You are an elite software engineering instructor. Walk through the code step-by-step and explain its purpose clearly."
    else:
        system_instruction = "You are a senior debugging assistant. Identify syntax or logical bugs, explain why they occur, and provide the corrected version inside markdown blocks."

    prompt = f"""
    Context: {system_instruction}
    Code Snippet:
    ```
    {code_snippet}
    ```
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

# ---------------------------------------------------------
# STREAMLIT USER INTERFACE (UI)
# ---------------------------------------------------------

st.title("🤖 Gemini AI Multi-Tool Workspace")
st.write("Switch between tabs below to use different features built using the Google GenAI SDK.")

# Create individual tabs for each feature requirement
tab1, tab2, tab3 = st.tabs(["💬 Basic Chat", "✉️ Smart Email Writer", "💻 Code Explainer & Debugger"])

# --- TAB 1: BASIC CHAT ---
with tab1:
    st.subheader("Feature 1: Basic Chat")
    chat_prompt = st.text_input("Ask Gemini anything:", placeholder="e.g., Explain what an API is in one sentence with an analogy.")
    
    if st.button("Send Message", key="btn_chat", type="primary"):
        if chat_prompt.strip():
            with st.spinner("Thinking..."):
                reply = basic_chat(chat_prompt)
                st.markdown(reply)
        else:
            st.warning("Please enter a prompt first.")

# --- TAB 2: SMART EMAIL WRITER ---
with tab2:
    st.subheader("Feature 2: Smart Email Writer")
    
    col1, col2 = st.columns(2)
    with col1:
        sender = st.text_input("Your Name:", value="Your Name")
        recipient = st.text_input("Recipient:", value="Manager")
    with col2:
        purpose = st.text_input("Purpose of Email:", value="request sick leave")
        tone = st.selectbox("Tone:", ["formal", "casual", "urgent", "polite"])
        
    points_input = st.text_area(
        "Key Points (One per line):", 
        value="Feeling unwell since morning\nWill be unavailable today\nWill catch up on work tomorrow"
    )
    
    if st.button("Generate Email", key="btn_email", type="primary"):
        key_list = [p.strip() for p in points_input.split("\n") if p.strip()]
        with st.spinner("Drafting email..."):
            generated_email = write_email(purpose, recipient, tone, key_list, sender)
            st.text_area("Generated Output:", value=generated_email, height=300)

# --- TAB 3: CODE EXPLAINER & DEBUGGER ---
with tab3:
    st.subheader("Feature 3: Code Explainer & Debugger")
    
    mode_selection = st.radio(
        "Select Operation Mode:",
        options=["Explain Functionality", "Identify & Fix Bugs"],
        horizontal=True
    )
    selected_mode = "explain" if mode_selection == "Explain Functionality" else "debug"
    
    code_input = st.text_area(
        "Paste Code Here:", 
        placeholder="def calculate_average(numbers)\ntotal = sum(numbers)\n    return total / len(numbers)",
        height=200
    )
    
    if st.button("Analyze Code", key="btn_code", type="primary"):
        if code_input.strip():
            with st.spinner("Analyzing code..."):
                analysis = explain_code(code_input, mode=selected_mode)
                st.