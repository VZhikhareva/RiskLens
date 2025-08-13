# service.py
# RiskService — calls OpenAI and validates the JSON into RiskReport.

import os
from dotenv import load_dotenv
from openai import OpenAI
from models import RiskReport

def build_system_prompt() -> str:
    return """
You are an assistant that outputs ONLY valid JSON according to this schema:

RiskReport:
- items: list[RiskItem]

RiskItem:
- risk: string, short human-readable title of the risk
- category: one of ["Compliance/Legal","Privacy/Data","Security","Operational","Financial/Fraud","Safety/Clinical","Model/AI"]
- severity: integer 1-5 (impact level)
- likelihood: integer 1-5 (probability level)
- controls: list of strings
- evidence: list of strings
- standards: list of strings (e.g., HIPAA, GDPR, SOX)
- owner: optional string
- time_horizon: optional, one of ["immediate","quarter","year"]

Hard rules:
- Output MUST be pure JSON without any explanation or extra text.
- All fields MUST be present, even if empty.
- Each risk MUST include at least one evidence quote that appears in the scenario text.
"""


class RiskService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing in .env")
        self.model_id = os.getenv("MODEL_ID", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)

    def analyze(self, scenario_text: str) -> RiskReport:
        """Send scenario to the model and validate structured JSON into RiskReport."""
        messages = [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": f"Scenario:\n{scenario_text}\n\nReturn a RiskReport with 2-4 items."},
        ]

        resp = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=0,
        )
        raw = resp.choices[0].message.content

        # Validate against our Pydantic schema (raises if invalid)
        report = RiskReport.model_validate_json(raw)
        return report
