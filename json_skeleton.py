import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from models import RiskReport  # твой model.py

# 1. Load env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("MODEL_ID", "gpt-4o-mini")

# 2. Create client
client = OpenAI(api_key=api_key)

# 3. System prompt: strict JSON
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

scenario = (
        "We collect patient intake forms via a web form and store them in S3. "
        "Analytics team and an external vendor have access. "
    )

# 4. Send request
response = client.chat.completions.create(
    model=model_id,
    messages=[
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": f"Scenario:\n{scenario}\n\nReturn a RiskReport with 1-4 items."},
    ],
    temperature=0
)

# 5. Get text from model
raw_text = response.choices[0].message.content

# 6. Try to parse JSON into Pydantic model
try:
    report = RiskReport.model_validate_json(raw_text)
    print("Parsed RiskReport object:")
    print(report.model_dump_json(indent=2))
except Exception as e:
    print("Failed to parse JSON:", e)
    print("Model output was:")
    print(raw_text)
