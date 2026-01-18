import os
from typing import List
from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from models import Claim



class ClaimExtraction(BaseModel):
    claims: List[dict] = Field(description="List of extracted claims")


class ClaimExtractor:
    def __init__(self, api_key: str = None):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.0,
            groq_api_key=api_key or os.getenv("GROQ_API_KEY")
        )
        
        self.parser = JsonOutputParser(pydantic_object=ClaimExtraction)

    def extract_claims(self, text: str, page_num: int = 1) -> List[Claim]:
        extraction_prompt = PromptTemplate(
            template = """You are an expert at identifying factual, checkable claims.

Extract ONLY specific, verifiable claims from the following text that contain:
- Numbers, statistics, or percentages
- Dates or specific time periods
- Financial figures, prices, or market caps
- Economic indicators (GDP, inflation, unemployment, etc.)
- Technical launch dates or failure counts

IGNORE:
- Generic explanations
- Definitions like "general information is..."
- Opinions or vague statements

For each claim, provide:
1. "claim_text": the exact claim text
2. "claim_type": STATISTIC, DATE, PRICE, FIGURE, PERCENTAGE, or TECHNICAL
3. "confidence": your confidence (0.0-1.0) in the extraction

Return a JSON object with a "claims" array.

Text to analyze:
{text}

JSON Response:""",
            input_variables=["text"]
        )

        chain = extraction_prompt | self.llm | self.parser
        result = chain.invoke({"text": text})

        claims = []
        for idx, claim_data in enumerate(result.get("claims", []), 1):
            claims.append(
                Claim(
                    id=idx,
                    text=claim_data.get("claim_text", ""),
                    claim_type=claim_data.get("claim_type", "UNKNOWN"),
                    extraction_confidence=float(claim_data.get("confidence", 0.7)),
                    page_number=page_num
                )
            )

        return claims
