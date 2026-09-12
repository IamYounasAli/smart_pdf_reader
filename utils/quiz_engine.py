import json
from utils.groq_client import get_groq_client

def generate_quiz(text: str, user_description: str, num_questions: int = 5) -> list:
    client = get_groq_client()
    
    system_prompt = """You are an educational AI assistant that creates multiple-choice quizzes from text.
You MUST output ONLY valid JSON format with NO markdown formatting, NO backticks, and NO conversational text.

Required JSON Structure:
[
  {
    "id": 1,
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A",
    "explanation": "Brief explanation of why this is correct."
  }
]"""

    user_prompt = f"""Generate {num_questions} multiple-choice questions based on the following document content.
Focus areas based on user context: {user_description}

--- DOCUMENT CONTENT ---
{text[:25000]}"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    raw_response = response.choices[0].message.content.strip()
    
    # Cleaning fallback if markdown backticks were added
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:-3].strip()
    elif raw_response.startswith("```"):
        raw_response = raw_response[3:-3].strip()

    data = json.loads(raw_response)
    if isinstance(data, dict) and "questions" in data:
        return data["questions"]
    elif isinstance(data, list):
        return data
    else:
        for v in data.values():
            if isinstance(v, list):
                return v
        raise ValueError("Could not parse valid questions array from LLM response.")
