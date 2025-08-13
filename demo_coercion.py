from models import RiskReport

report = RiskReport(items=[
    {
        "risk": "   Data leak   ",   # spaces → cut spaces
        "category": "Privacy/Data",
        "severity": "5",             # str →  int
        "likelihood": 2,
        "controls": [],
        "evidence": ['"S3 bucket open to vendor"'],
        "standards": ["GDPR"],
    },
    {
        "risk": "   Data leak   ",   
        "category": "Operational",
        "severity": 5,             
        "likelihood": 2,
        "controls": [],
        "evidence": ['"S3 bucket open to vendor"'],
        "standards": ["GDPR"],
    }
])

print(type(report.items[0]).__name__)   
print(report.items[1].category)             
print(report.model_dump_json(indent=2))
