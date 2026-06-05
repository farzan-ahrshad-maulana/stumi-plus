from pydantic import BaseModel


class ValidationResult(BaseModel):
    is_research_paper: bool
    confidence: float
    reason: str
