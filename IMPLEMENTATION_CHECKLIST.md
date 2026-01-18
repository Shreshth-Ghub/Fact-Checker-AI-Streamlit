# Fact-Checking Web App - Implementation Checklist

## ✓ Complete Codebase (Ready to Use)

### Core Modules
- [x] `models.py` - Claim and VerificationResult data classes
- [x] `pdf_processor.py` - PDF text extraction utilities  
- [x] `claim_extractor.py` - LLM-based claim identification
- [x] `fact_checker.py` - Verification logic with Tavily search
- [x] `app.py` - Streamlit UI with 3-tab interface

### Configuration Files
- [x] `requirements.txt` - All dependencies pinned
- [x] `README.md` - Complete documentation
- [x] `.env.example` - Environment template
- [x] `.streamlit/config.toml` - Streamlit configuration

### Architecture Decisions
- [x] LangChain for orchestration
- [x] OpenAI GPT-4o-mini for cost-efficient LLM tasks
- [x] Tavily API for live web search
- [x] Streamlit for frontend with 3-tab workflow
- [x] Pydantic models for type safety
- [x] Pandas for results table + CSV export

## Setup Instructions (When You Return)

### 1. Local Setup
```bash
mkdir fact-checker-ai
cd fact-checker-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Copy all .py files to this directory
# Copy requirements.txt
# Run:
pip install -r requirements.txt
```

### 2. API Keys
- Get OpenAI key from: https://platform.openai.com/api-keys
- Get Tavily key from: https://tavily.com (free tier available)
- Create `.env` file and add:
  ```
  OPENAI_API_KEY=sk-...
  TAVILY_API_KEY=tvly-...
  ```

### 3. Run Locally
```bash
streamlit run app.py
```

### 4. Test with Market Report PDF
- Use the attached "Assessment-Reference_Market_Report.pdf"
- App will extract ~8-12 claims
- Verify each against live web data
- Check if app catches outdated stats (e.g., Bitcoin price, GDP, unemployment)

## Quick Code Overview

**app.py**: 
- 3-tab interface: Upload/Extract → Verify → Results
- Manages session state for multi-step workflow
- Shows progress during verification
- CSV export of results

**claim_extractor.py**:
- Extracts claims from raw text using GPT-4o-mini
- JSON-structured output with claim_type and confidence
- Supports: STATISTIC, DATE, PRICE, FIGURE, PERCENTAGE, TECHNICAL

**fact_checker.py**:
- Takes a claim, searches web using Tavily
- Uses LLM to reason about verification
- Returns: status (VERIFIED/INACCURATE/FALSE) + correct_value + source

**models.py**:
- `Claim`: id, text, type, confidence, page_num
- `VerificationResult`: claim_id, status, correct_value, source_url, reasoning, confidence

**pdf_processor.py**:
- `extract_text_from_pdf()`: Returns full text + page count
- `extract_text_by_pages()`: Returns list of (page_num, text)

## Performance Expectations

- **Claim Extraction**: ~5-10 seconds per page
- **Verification**: ~30-60 seconds per claim (web search + LLM reasoning)
- **Total for 10 claims**: ~5-10 minutes
- **API costs**: ~$0.02-0.05 per PDF document

## Next Steps When You Return

1. Create GitHub repo with all files
2. Set up Streamlit Cloud deployment
3. Add API keys to Streamlit Cloud secrets
4. Deploy and test with the market report PDF
5. Record 30-second demo video
6. Submit to Cog Culture

---

**Status**: Production-ready code, waiting for API keys and deployment.
**Estimated Submission Time**: 15 minutes (GitHub + Streamlit Cloud + video)
