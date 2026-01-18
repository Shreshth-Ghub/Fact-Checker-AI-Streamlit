# Fact Checker AI 🔍

Automated Streamlit app that extracts claims from PDFs and fact-checks them against live web data with a verification dashboard and CSV export.

## Overview

Fact Checker AI is a production-ready web application that automatically extracts factual claims from PDF reports and verifies them against live web data. It then presents a verification dashboard with status labels and confidence scores, plus an exportable CSV for reporting. 

**⚠️ Note**: Verification scores are **indicative**, not absolute truth. This is an automated system.

## Features

- **PDF Upload & Processing**  
  Drag‑and‑drop interface to upload reports in PDF format.

- **Intelligent Claim Extraction**  
  Automatically detects statistics, dates, prices, and other verifiable claims from the document.

- **Live Web Verification**  
  Checks each extracted claim against current information from the web.

- **Three‑Level Verdicts**  
  Classifies claims as **VERIFIED**, **INACCURATE**, or **FALSE** with reasoning and source URLs.

- **Results Dashboard**  
  Modern dark‑glass UI showing cards for verified / inaccurate / false counts and average confidence, plus a compact results table.

- **CSV Export**  
  Download all verification results as a CSV file for further analysis or reporting.

- **Deployment Ready**  
  Single‑command run locally and easy deployment to Streamlit Community Cloud.

## Tech Stack

- **Frontend / UI**: Streamlit with custom dark glassmorphism CSS  
- **Backend Logic**: Python (custom `PDFProcessor`, `ClaimExtractor`, `FactChecker` classes)  
- **PDF Processing**: `PyPDF2` / pdfplumber for text extraction  
- **Data Handling**: `pandas` for results aggregation and export  
- **Environment & Packaging**: `requirements.txt` for reproducible installs

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fact-checker-ai-streamlit.git
cd fact-checker-ai-streamlit
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Set up environment variables

If your `FactChecker` uses external APIs or keys, create a `.env` file or use `.streamlit/secrets.toml`:

```
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

Keep these out of Git by adding them to `.gitignore`.

## Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Project Structure

```text
fact-checker-ai-streamlit/
├── app.py                 # Main Streamlit application (UI + workflow)
├── pdf_processor.py       # PDF text extraction utilities
├── claim_extractor.py     # Claim extraction from raw PDF text
├── fact_checker.py        # Claim verification and web searching logic
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file (Python, venv, cache)
├── README.md             # Project documentation (this file)
└── samples/              # Example PDFs for testing (optional)
```

## How It Works

### Step 1: Upload & Extract

1. User uploads a PDF document from the **UPLOAD & EXTRACT** tab.
2. `PDFProcessor` extracts raw text and counts total pages.
3. `ClaimExtractor` parses the text and returns a list of structured claims.
4. Each claim includes extraction confidence scores.
5. User reviews extracted claims before proceeding to verification.

### Step 2: Verify Claims

1. From the **VERIFY CLAIMS** tab, the app iterates over each extracted claim.
2. `FactChecker` performs web searches and analyzes live data relevant to the claim.
3. For each claim, it returns:
   - **Status**: VERIFIED / INACCURATE / FALSE
   - **Correct Value**: The accurate information found
   - **Source URL**: Primary source used
   - **Reasoning**: Explanation of the determination
   - **Confidence Score**: 0–100% confidence level

### Step 3: Review Results

1. The **RESULTS** tab displays:
   - **Metric Cards**: Counts of verified, inaccurate, and false claims plus average confidence
   - **Results Table**: Compact, sortable view of all claims with their statuses
   - **CSV Export**: Download results for reporting or further analysis

## Deployment to Streamlit Community Cloud

1. **Push to GitHub**  
   Ensure your repository is public on GitHub.

2. **Go to Streamlit Cloud**  
   Navigate to [Streamlit Community Cloud](https://streamlit.io/cloud).

3. **Create New App**  
   Click "New app", select your GitHub repository, branch (`main`), and main file (`app.py`).

4. **Configure Secrets** *(if needed)*  
   In **App settings → Secrets**, add any required API keys (e.g., `OPENAI_API_KEY`, `TAVILY_API_KEY`).

5. **Deploy**  
   Click deploy and share your public URL.

**Your live app will be:** `https://yourusername-fact-checker-ai.streamlit.app`

## API & Cost Estimates

### Optional: OpenAI Integration (if used)

- **Model**: gpt-4o-mini (cost-effective)
- **Usage**: Claim extraction + verification reasoning
- **Estimated Cost**: $0.01–0.05 per PDF (depending on length)

### Optional: Tavily Search (if used)

- **Free tier** available for development
- **Cost**: Minimal for small-scale usage
- **Searches per verification**: ~5 per claim

*(Actual implementation may differ; refer to your `fact_checker.py` for specifics.)*

## Example Use Cases

- **News Verification**: Fact‑check articles before publication
- **Financial Reports**: Verify numbers and statements in market research
- **Government Statistics**: Cross‑reference official claims across sources
- **Academic Projects**: Demonstrate NLP + web data verification
- **Internship Portfolio**: Showcase full‑stack AI application development

## Verification Logic Overview

The verification process uses a multi‑step approach:

1. **Query Refinement**: Complex claims are condensed into searchable queries
2. **Web Search**: Retrieves relevant current information from the web
3. **LLM Analysis**: Compares original claim against search results
4. **Classification**: Status determined based on evidence
5. **Source Attribution**: Primary source URL extracted and linked

## Performance Notes

- **Processing Time**: 2–5 minutes for 10–15 claims (depends on PDF length and search latency)
- **Cost Estimate**: $0.02–0.10 per document (if using paid APIs)
- **Accuracy**: Depends on search result availability and LLM reasoning quality

## Limitations

- Claims must be verifiable via web search (proprietary/internal data won't work)
- Complex technical claims may require domain expertise
- Real‑time events not yet indexed by search engines may not be found
- API rate limits apply to both search and LLM services
- Very niche or local information has limited availability online

## Future Enhancements

- Multi‑language claim extraction and verification
- Batch PDF processing for bulk document analysis
- Source credibility scoring and filtering
- Richer visual analytics for confidence patterns
- Integration with academic databases (arXiv, Google Scholar)
- Historical fact verification (archive search support)
- Advanced reason visualization with charts/graphs

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

MIT License — see `LICENSE` file for details.

## Support & Feedback

For issues, questions, or feature requests, please open a **GitHub Issue** on the repository.

## Author

Created as part of **Cog Culture AI Internship Assignment** and as a portfolio project showcasing:

- Full‑stack Streamlit application development
- NLP and claim extraction techniques
- Live web data integration
- Modern UI/UX with custom CSS
- Deployment and DevOps practices

---

**Happy fact‑checking! 🔍✨**
