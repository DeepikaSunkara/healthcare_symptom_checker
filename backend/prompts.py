# prompts.py
from typing import Dict

SYSTEM_INSTRUCTION = """
You are a medical-knowledgeable assistant for educational purposes only.
When given a list of symptoms, produce JSON with the following keys:
- probable_conditions: an array of objects with {condition, likelihood (High/Medium/Low), reasons}.
- recommended_next_steps: an array of short bullet steps (e.g., seek immediate care, see GP, monitor at home, tests).
- red_flags: an array of urgent signs that require emergency care.
- disclaimer: a short educational disclaimer.

Respond ONLY with valid JSON.
"""

def build_messages(symptoms: str, patient_info: Dict | None = None) -> list:
    """
    Returns an OpenAI/Groq-compatible messages list for the chat completion API.
    """
    user_prompt = f"""Patient symptoms: {symptoms}

Patient info (if provided): {patient_info}

Output format requirements:
1) JSON object with keys: probable_conditions, recommended_next_steps, red_flags, disclaimer.
2) probable_conditions must contain at least 2-4 candidate conditions with brief reasoning.
3) recommended_next_steps must be actionable and mention when to see a doctor.
4) Keep answers concise. This is educational only.
"""
    return [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": user_prompt}
    ]
