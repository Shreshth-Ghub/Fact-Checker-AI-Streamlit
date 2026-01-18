from dotenv import load_dotenv
load_dotenv()

from models import Claim
from fact_checker import FactChecker

claim = Claim(
    id=1,
    text="As of January 2026, Bitcoin is trading at roughly 42,500 and struggling to break the 45k resistance level.",
    claim_type="PRICE",
    extraction_confidence=0.95,
    page_number=1,
)

checker = FactChecker()
result = checker.verify_claim(claim)
print("STATUS:", result.status)
print("CORRECT_VALUE:", result.correct_value)
print("SOURCE:", result.source_url)
print("REASONING:", result.reasoning)
