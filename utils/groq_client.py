import os
from groq import Groq

def get_groq_client(api_key: str = None) -> Groq:
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("Groq API key not provided or found in environment variables.")
    return Groq(api_key=key)

def generate_analysis(text: str, user_description: str, mode: str, api_key: str = None) -> str:
    client = get_groq_client(api_key)
    
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
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=2048
    )
    
    return response.choices[0].message.content
