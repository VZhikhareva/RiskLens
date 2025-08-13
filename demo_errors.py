from models import RiskItem
from pydantic import ValidationError

cases = [
    # wrong category
    dict(risk="Something", category="Random", severity=3, likelihood=2),

    # severity exceeds 1–5
    dict(risk="Bad severity", category="Security", severity=10, likelihood=2),

    # empty risk after strip()
    dict(risk="   ", category="Security", severity=2, likelihood=2),
]

for i, data in enumerate(cases, 1):
    try:
        RiskItem(**data)
        print(f"Case {i}: OK")
    except ValidationError as e:
        print(f"\nCase {i}: ValidationError")
        print(e)