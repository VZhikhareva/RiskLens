# demo_ok.py
# Goal: create valid objects and serialize them to JSON.

from models import RiskItem, RiskReport

item = RiskItem(
    risk="Unauthorized data access",
    category="Security",
    severity=4,
    likelihood=3,
    controls=["RBAC", "Least privilege"],
    evidence=['"analytics team and contractor have access"'],
    standards=["SOC2"],
    owner="Security Lead",
    time_horizon="quarter",
)

report = RiskReport(items=[item])

# Pretty JSON string
print(report.model_dump_json(indent=2))

# (Optional) also show Python dict
# print(report.model_dump())