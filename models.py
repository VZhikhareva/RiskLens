from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional

Category = Literal[
    "Compliance/Legal",
    "Privacy/Data",
    "Security",
    "Operational",
    "Financial/Fraud",
    "Safety/Clinical",
    "Model/AI",
]

class RiskItem(BaseModel):
    risk: str = Field(..., description="Short, human-readable risk title")
    category: Category
    severity: int = Field(..., ge=1, le=5, description="Impact 1-5")
    likelihood: int = Field(..., ge=1, le=5, description="Probability 1-5")
    controls: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list, description="Verbatim quotes from input")
    standards: List[str] = Field(default_factory=list, description="e.g., HIPAA, GDPR, SOX")
    owner: Optional[str] = Field(default=None, description="Responsible role")
    time_horizon: Optional[Literal["immediate", "quarter", "year"]] = None
    
    @field_validator("risk")
    @classmethod
    def trim_title(cls, v: str) -> str:
        t = v.strip()
        if not t:
            raise ValueError("risk title must be non-empty")
        return t
    
class RiskReport(BaseModel):
    items: List[RiskItem] = Field(default_factory=list)