# Fact-Checking Web App - Architecture Design

## System Architecture

```
PDF Upload
    ↓
PyPDF2/pdfplumber → Extract Raw Text
    ↓
LangChain + OpenAI → Extract Structured Claims
    ↓
Claim Processor (Batch)
    ├─ For each claim:
    │   ├─ Tavily Search API → Get live web data
    │   ├─ LangChain Agent → Verify against web results
    │   └─ Generate: Verification Status + Correct Value + Source
    ↓
Results Aggregator
    ├─ Status: VERIFIED | INACCURATE | FALSE
    ├─ Original Claim
    ├─ Correct Value
    ├─ Source URL
    └─ Confidence Score
    ↓
Streamlit UI → Display Results Table
    └─ Export to CSV
```

## Data Structures

### Extracted Claim
```python
class Claim:
    id: int
    text: str
    claim_type: str  # "STATISTIC" | "DATE" | "PRICE" | "FIGURE"
    extraction_confidence: float
    page_number: int
```

### Verification Result
```python
class VerificationResult:
    claim_id: int
    original_claim: str
    status: str  # "VERIFIED" | "INACCURATE" | "FALSE"
    correct_value: str
    source_url: str
    reasoning: str
    confidence_score: float
    verified_at: datetime
```

## LangChain Agent Flow

1. **Claim Extraction Agent**
   - Input: Raw PDF text
   - Task: Identify claims with type and confidence
   - Output: List[Claim]

2. **Verification Agent**
   - Input: Single Claim + Tavily Search Results
   - Task: Determine accuracy using web data
   - Output: VerificationResult

## API Integration

### Tavily Search
- Query: Refined claim question
- Returns: Top 5-10 results with snippets
- Used by: Verification Agent

### OpenAI
- Model: gpt-4o-mini (cost-effective)
- Used for:
  - Claim extraction from PDF
  - Verification reasoning
  - Value correction

## Deployment

- **Streamlit Cloud**: Free, auto-deploys from GitHub
- **GitHub**: Source code + requirements.txt + README
- **Environment**: Python 3.10+, pip dependencies
