import os
import streamlit as st
from groq import Groq

def get_groq_client() -> Groq:
    # 1. Safe secret check to prevent StreamlitSecretNotFoundError
    key = None
    try:
        key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass
        
    key = key or os.environ.get("GROQ_API_KEY")
    
    if not key:
        raise ValueError("GROQ_API_KEY is missing. Add it under Settings > Secrets in Streamlit Cloud.")
        
    return Groq(api_key=key)

def generate_analysis(text: str, user_description: str, mode: str) -> str:
    client = get_groq_client()
    
    prompts = {
        "summary": "Provide a detailed executive summary of the text. User Context: {description}",
        "skimming": "Provide key headings and main arguments for skimming. User Context: {description}",
        "scanning": "Extract key metrics, dates, and terms for scanning. User Context: {description}"
    }
    
    system_prompt = "You are an expert document analyzer."
    user_prompt = f"{prompts.get(mode, prompts['summary']).format(description=user_description)}\n\nDOCUMENT:\n{text[:20000]}"
    
    # Updated model string
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content
