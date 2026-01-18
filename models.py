from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


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

    def to_dict(self):
        d = asdict(self)
        d['verified_at'] = d['verified_at'].isoformat()
        return d
