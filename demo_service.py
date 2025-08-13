# demo_service.py
# Quick test for RiskService with dummy output.

from service import RiskService

svc = RiskService()

scenario = "We store patient medical forms in S3, accessible by analytics team and vendor."
report = svc.analyze(scenario)

# Print the validated JSON representation of the report
print(report.model_dump_json(indent=2))