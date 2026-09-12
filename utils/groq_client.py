import os
import streamlit as st
from groq import Groq

def get_groq_client() -> Groq:
    # Fetch from Streamlit Cloud Secrets or local environment variables
    key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    
    if not key:
        raise ValueError("GROQ_API_KEY is missing. Please add it to your Streamlit Cloud Secrets.")
        
    return Groq(api_key=key)

def generate_analysis(text: str, user_description: str, mode: str) -> str:
    client = get_groq_client()
    
    prompts = {
        "summary": """Provide a comprehensive executive summary of the document below. 
Highlight the main theme, context, objectives, and overall conclusions.
Context provided by user: {description}""",
        
        "skimming": """Perform a skimming analysis of the document below.
Extract key headings, main bullet points, central arguments, and core takeaways for quick visual scanning.
Context provided by user: {description}""",
        
        "scanning": """Perform a detailed scanning analysis of the document below.
Locate and extract specific entities: key dates, numbers, statistical metrics, definitions, formulas, and technical terminology.
Context provided by user: {description}"""
    }
    
    system_prompt = "You are an expert AI document analyzer and researcher."
    user_prompt = f"{prompts.get(mode, prompts['summary']).format(description=user_description)}\n\n--- DOCUMENT CONTENT ---\n{text[:25000]}"
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=2048
    )
    
    return response.choices[0].message.content
