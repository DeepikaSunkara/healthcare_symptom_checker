# app.py
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
from prompts import build_messages

load_dotenv()  # reads .env

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_ID = os.getenv("MODEL_ID", "llama-3.1-8b-instant")  # default

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set. Copy .env.example -> .env and set your key.")

app = FastAPI(title="Healthcare Symptom Checker (Educational)")

class SymptomRequest(BaseModel):
    symptoms: str
    patient_info: dict | None = None
    temperature: float | None = 0.0

class SymptomResponse(BaseModel):
    probable_conditions: list
    recommended_next_steps: list
    red_flags: list
    disclaimer: str
    raw_model_text: str | None = None

@app.post("/api/symptom-check", response_model=SymptomResponse)
async def symptom_check(req: SymptomRequest):
    # Build messages
    messages = build_messages(req.symptoms, req.patient_info)
    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": req.temperature or 0.0,
        "max_tokens": 800
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    endpoint = f"{GROQ_BASE}/chat/completions"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(endpoint, json=payload, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Model API error: {resp.status_code} - {resp.text}")
        data = resp.json()

    # Groq's chat response can vary. Try to extract text.
    # Docs show the top-level response contains choices/messages similar to OpenAI.
    # Example extraction below:
    # Try multiple locations for the model text
    model_text = None
    if "choices" in data and len(data["choices"]) > 0:
        # chat style: choices[0].message.content
        choice = data["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            model_text = choice["message"]["content"]
        elif "text" in choice:
            model_text = choice["text"]
    # fallback: top-level text
    if not model_text:
        model_text = json.dumps(data)

    # Attempt to parse JSON from model_text
    parsed = None
    try:
        parsed = json.loads(model_text)
    except Exception:
        # Try to extract first JSON substring from text
        import re
        m = re.search(r'(\{(?:.|\n)*\})', model_text)
        if m:
            try:
                parsed = json.loads(m.group(1))
            except Exception:
                parsed = None

    if not parsed:
        # If parsing fails, still return model_text with a default structure
        return {
            "probable_conditions": [],
            "recommended_next_steps": [],
            "red_flags": [],
            "disclaimer": "Model response could not be parsed. Please try again with clearer symptoms.",
            "raw_model_text": model_text
        }

    # Validate structure and return
    return {
        "probable_conditions": parsed.get("probable_conditions", []),
        "recommended_next_steps": parsed.get("recommended_next_steps", []),
        "red_flags": parsed.get("red_flags", []),
        "disclaimer": parsed.get("disclaimer", "This is educational information and not medical advice."),
        "raw_model_text": model_text
    }
