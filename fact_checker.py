import os
from typing import List
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
from tavily import TavilyClient
from models import Claim, VerificationResult
import re


class FactChecker:
    def __init__(self, groq_api_key: str = None, tavily_api_key: str = None):
        self.client = Groq(api_key=groq_api_key or os.getenv("GROQ_API_KEY"))
        self.tavily = TavilyClient(api_key=tavily_api_key or os.getenv("TAVILY_API_KEY"))

    def verify_claim(self, claim: Claim) -> VerificationResult:
        search_query = self._build_search_query(claim.text)

        try:
            search_results = self.tavily.search(
                query=search_query,
                max_results=5,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=False,
            )
        except Exception as e:
            search_results = {"results": [], "answer": None}

        search_context = self._format_search_results(search_results)

        prompt = f"""You are a fact-checking expert. Analyze this claim against live web search data.

CLAIM: {claim.text}
CLAIM TYPE: {claim.claim_type}

WEB DATA:
{search_context}

YOUR TASK:
1. Compare the claim against web results
2. If web data contradicts or differs from claim → INACCURATE or FALSE
3. Treat the claim as about the CURRENT situation unless the date is explicitly historical.
4. If current web data is different from the claim's numbers or dates, mark it INACCURATE even if it might have been true in the past.
5. If no web data available → FALSE (cannot verify).

RESPOND WITH EXACTLY THIS FORMAT (no extra text):
STATUS: VERIFIED|INACCURATE|FALSE
CORRECT_VALUE: [actual value from web or N/A]
SOURCE_URL: [best URL or N/A]
REASONING: [1-2 sentences why]
CONFIDENCE: [0.0 to 1.0]"""

        try:
            chat = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300,
            )
            verification_text = chat.choices[0].message.content
        except Exception as e:
            verification_text = f"STATUS: FALSE\nCORRECT_VALUE: Verification failed\nSOURCE_URL: N/A\nREASONING: LLM error: {str(e)}\nCONFIDENCE: 0.0"

        return self._parse_verification_response(claim, verification_text)

    def _build_search_query(self, claim_text: str) -> str:
        text = (claim_text or "").strip()
        if not text:
            return "general information"
        if len(text) > 150:
            text = text[:150]
        return text

    def _format_search_results(self, results) -> str:
        if not results:
            return "No search results available."

        parts = []

        answer = results.get("answer")
        if answer:
            parts.append(f"SUMMARY: {answer}")

        res_list = results.get("results", [])
        if res_list:
            parts.append("SEARCH RESULTS:")
            for i, res in enumerate(res_list[:5], 1):
                title = (res.get("title") or "")[:100]
                content = (res.get("content") or "")[:250]
                url = res.get("url", "")
                parts.append(f"  [{i}] {title}\n      {content}\n      URL: {url}")

        return "\n".join(parts) if parts else "No search results available."

    def _parse_verification_response(self, claim: Claim, text: str) -> VerificationResult:
        status = self._extract_field(text, "STATUS", "FALSE").upper()
        if status not in ["VERIFIED", "INACCURATE", "FALSE"]:
            status = "FALSE"

        correct_value = self._extract_field(text, "CORRECT_VALUE", "Unable to verify")
        source_url = self._extract_field(text, "SOURCE_URL", "N/A")
        reasoning = self._extract_field(text, "REASONING", "No reasoning provided")
        confidence = self._extract_confidence(text)

        return VerificationResult(
            claim_id=claim.id,
            original_claim=claim.text,
            status=status,
            correct_value=correct_value,
            source_url=source_url,
            reasoning=reasoning,
            confidence_score=confidence,
            verified_at=datetime.now(),
        )

    def _extract_field(self, text: str, field_name: str, default: str) -> str:
        pattern = rf"{field_name}:\s*(.+?)(?:\n|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            return value if value else default
        return default

    def _extract_confidence(self, text: str) -> float:
        match = re.search(r"CONFIDENCE:\s*([\d.]+)", text, re.IGNORECASE)
        if match:
            try:
                conf = float(match.group(1))
                return min(max(conf, 0.0), 1.0)
            except (ValueError, TypeError):
                return 0.5
        return 0.5