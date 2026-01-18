# Fact-Checking Web App

## Overview

A production-ready AI-powered web application that automatically extracts factual claims from PDFs and verifies them against live web data using OpenAI and Tavily Search APIs. This is an automated system verification scores are indicative, not absolute truth.

## Features

- **PDF Upload & Processing**: Drag-and-drop interface for uploading PDFs
- **Intelligent Claim Extraction**: Uses GPT-4o-mini to identify statistics, dates, prices, and other verifiable claims
- **Live Web Verification**: Cross-references extracted claims against real-time web data using Tavily Search API
- **Three-Level Verification**: Classifies claims as VERIFIED, INACCURATE, or FALSE
- **Results Dashboard**: View results in an interactive table with CSV export
- **Deployment Ready**: Single-command deployment to Streamlit Cloud

## Tech Stack

- **Frontend**: Streamlit
- **Backend Logic**: LangChain with OpenAI GPT-4o-mini
- **Web Search**: Tavily API
- **PDF Processing**: pdfplumber
- **Data Handling**: Pandas, Pydantic

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fact-checker-ai.git
cd fact-checker-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

## Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── models.py             # Data models (Claim, VerificationResult)
├── claim_extractor.py    # PDF claim extraction logic
├── fact_checker.py       # Verification and web search logic
├── pdf_processor.py      # PDF text extraction utilities
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .env                 # Environment variables (not committed)
```

## How It Works

### Step 1: Upload & Extract
- Upload a PDF document
- App extracts raw text from all pages
- GPT-4o-mini identifies specific verifiable claims (statistics, dates, prices, etc.)
- User reviews extracted claims before verification

### Step 2: Verify Claims
- For each extracted claim:
  - Tavily Search API retrieves top 5 relevant web results
  - GPT-4o-mini analyzes search results against the original claim
  - Assigns verification status: VERIFIED, INACCURATE, or FALSE
  - Extracts the correct value and primary source URL
  - Calculates confidence score

### Step 3: Review Results
- Interactive table displaying all verification results
- Metrics dashboard showing verified/inaccurate/false counts
- CSV export for reporting and further analysis

## API Requirements

### OpenAI API
- Model: gpt-4o-mini (cost-effective, fast)
- Usage: Claim extraction + verification reasoning
- Estimated cost: $0.01-0.05 per PDF (depending on length and number of claims)

### Tavily API
- Free tier available for development
- Usage: Live web search for claim verification
- Searches per verification: ~5 per claim

## Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app" and select your repository
4. Set environment variables (OPENAI_API_KEY, TAVILY_API_KEY) in Streamlit Cloud settings
5. Deploy

Live URL will be: `https://yourusername-fact-checker-ai.streamlit.app`

## Verification Logic

The verification process uses a multi-step approach:

1. **Query Refinement**: Long claims are condensed into searchable queries
2. **Web Search**: Tavily API retrieves relevant current information
3. **LLM Analysis**: GPT-4o-mini compares the original claim against search results
4. **Classification**: Status is determined based on matching current data
5. **Source Attribution**: Primary source URL is extracted from search results

## Example Use Cases

- News article fact-checking before publication
- Financial report accuracy verification
- Technical documentation claim validation
- Market research document verification
- Government statistics cross-reference

## Performance Notes

- **Processing Time**: 2-5 minutes for 10-15 claims (depends on PDF length and search latency)
- **Cost Estimate**: $0.02-0.10 per document with Tavily free tier + gpt-4o-mini
- **Accuracy**: Depends on search result availability and LLM reasoning quality

## Limitations

- Claims must be verifiable via web search (local/proprietary data won't work)
- Complex technical claims may require domain expertise to verify accurately
- Real-time events not yet indexed by search engines may not be found
- API rate limits apply to both OpenAI and Tavily

## Future Enhancements

- Multi-language support
- Historical fact verification (archive search)
- Source credibility scoring
- Batch PDF processing
- Integration with academic databases
- Confidence interval visualization

## License

MIT License

## Support

For issues, questions, or feature requests, please open a GitHub issue.

## Author

Created for Cog Culture AI Internship Assignment
