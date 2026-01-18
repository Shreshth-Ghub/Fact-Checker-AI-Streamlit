from dataclasses import dataclass
from datetime import datetime

@dataclass
class Claim:
    id: int
    text: str
    claim_type: str
    extraction_confidence: float
    page_number: int

@dataclass
class VerificationResult:
    claim_id: int
    original_claim: str
    status: str
    correct_value: str
    source_url: str
    reasoning: str
    confidence_score: float
    verified_at: datetime
