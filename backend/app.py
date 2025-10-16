# app.py
import os
import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from prompts import build_messages
import datetime

# Load environment
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_ID = os.getenv("MODEL_ID", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set. Copy .env.example -> .env and set your key.")

app = FastAPI(title="Healthcare Symptom Checker (Educational)")

# ----------------------------
# Database setup
# ----------------------------
DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QueryHistory(Base):
    __tablename__ = "query_history"
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    ai_output = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Request/Response models
# ----------------------------
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

# ----------------------------
# Routes
# ----------------------------
@app.post("/api/symptom-check", response_model=SymptomResponse)
async def symptom_check(req: SymptomRequest, db: Session = Depends(get_db)):
    # Build messages for Groq
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

    # Extract model text
    model_text = None
    if "choices" in data and len(data["choices"]) > 0:
        choice = data["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            model_text = choice["message"]["content"]
        elif "text" in choice:
            model_text = choice["text"]
    if not model_text:
        model_text = json.dumps(data)

    # Attempt to parse JSON from model_text
    parsed = None
    try:
        parsed = json.loads(model_text)
    except Exception:
        import re
        m = re.search(r'(\{(?:.|\n)*\})', model_text)
        if m:
            try:
                parsed = json.loads(m.group(1))
            except Exception:
                parsed = None

    # Default response if parsing fails
    response_data = {
        "probable_conditions": parsed.get("probable_conditions", []) if parsed else [],
        "recommended_next_steps": parsed.get("recommended_next_steps", []) if parsed else [],
        "red_flags": parsed.get("red_flags", []) if parsed else [],
        "disclaimer": parsed.get("disclaimer", "This is educational information and not medical advice.") if parsed else "Model response could not be parsed. Please try again with clearer symptoms.",
        "raw_model_text": model_text
    }

    # ----------------------------
    # Save query history
    # ----------------------------
    record = QueryHistory(user_input=req.symptoms, ai_output=model_text)
    db.add(record)
    db.commit()
    db.refresh(record)

    return response_data

# ----------------------------
# Endpoint to view history
# ----------------------------
@app.get("/api/history/")
def get_history(db: Session = Depends(get_db)):
    records = db.query(QueryHistory).order_by(QueryHistory.timestamp.desc()).all()
    return records
