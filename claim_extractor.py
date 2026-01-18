import os
from typing import List
from dotenv import load_dotenv
from groq import Groq
import json
import re

load_dotenv()

class ClaimExtractor:
    def __init__(self, api_key: str = None):
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))

    def extract_claims(self, text: str, page_num: int = 1) -> List[dict]:
        prompt = f"""Extract ONLY specific, verifiable claims from this text that contain:
- Numbers, statistics, or percentages
- Dates or specific time periods
- Financial figures, prices, or market caps
- Economic indicators (GDP, inflation, unemployment, etc.)

Return ONLY a valid JSON array like:
[
  {{"claim_text": "...", "claim_type": "PRICE", "confidence": 0.9}},
  {{"claim_text": "...", "claim_type": "STATISTIC", "confidence": 0.85}}
]

Text: {text[:3000]}"""

        chat = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=2000,
        )

        response = chat.choices[0].message.content.strip()
        
        try:
            claims_data = json.loads(response)
        except:
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                claims_data = json.loads(match.group(0))
            else:
                claims_data = []

        claims = []
        for idx, claim in enumerate(claims_data, 1):
            claims.append({
                "id": idx,
                "text": claim.get("claim_text", ""),
                "claim_type": claim.get("claim_type", "UNKNOWN"),
                "extraction_confidence": float(claim.get("confidence", 0.7)),
                "page_number": page_num
            })

        return claims
