# api.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from pathlib import Path
from service import RiskService
from models import RiskReport

app = FastAPI(title="RiskLens API", version="0.3.0")

@app.get("/health")
def health():
    return {"status": "ok"}

class AnalyzeIn(BaseModel):
    scenario: str = Field(..., min_length=1, description="Free-text scenario to analyze")

@app.post("/analyze", response_model=RiskReport)
def analyze(payload: AnalyzeIn):
    svc = RiskService()
    report = svc.analyze(payload.scenario)
    return report

# --- NEW: tiny HTML page with a form + JS ---
@app.get("/", response_class=HTMLResponse)
def home():
    return Path("home.html").read_text(encoding = "utf-8")

