import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

from pdf_processor import PDFProcessor
from claim_extractor import ClaimExtractor
from fact_checker import FactChecker


st.set_page_config(
    page_title="Fact Checker AI",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a0f3e 25%, #2d1b4e 50%, #1a0f3e 75%, #0a0e27 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    [data-testid="stAppViewContainer"] {
        background-attachment: fixed;
        background-size: 200% 200%;
    }

    .main {
        background: transparent;
        padding: 3rem 2rem;
    }

    .header-container {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.08) 0%, rgba(100, 50, 255, 0.08) 50%, rgba(255, 0, 150, 0.08) 100%);
        border: 2px solid rgba(0, 255, 200, 0.4);
        border-radius: 20px;
        padding: 3rem;
        margin-bottom: 2.5rem;
        text-align: center;
        backdrop-filter: blur(20px);
        box-shadow: 0 0 60px rgba(0, 255, 200, 0.2), inset 0 0 60px rgba(100, 50, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 255, 200, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    .header-container h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #00ffc8 0%, #6432ff 50%, #ff0096 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 255, 200, 0.3);
        position: relative;
        z-index: 1;
    }

    .header-container p {
        font-size: 1.1rem;
        color: rgba(0, 255, 200, 0.9);
        font-weight: 300;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }

    .tabs-container {
        margin-top: 2rem;
    }

    [data-testid="stTabs"] [role="tablist"] {
        background: linear-gradient(90deg, rgba(0, 255, 200, 0.05) 0%, rgba(100, 50, 255, 0.05) 100%);
        border-bottom: 2px solid rgba(0, 255, 200, 0.3);
        border-radius: 12px 12px 0 0;
        padding: 0.5rem;
        gap: 0.5rem;
        backdrop-filter: blur(15px);
    }

    [data-testid="stTabs"] [role="tab"] {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.05), rgba(100, 50, 255, 0.05));
        border: 1.5px solid rgba(0, 255, 200, 0.2);
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        color: rgba(200, 220, 255, 0.7);
        font-weight: 600;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    [data-testid="stTabs"] [role="tab"]:hover {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.15), rgba(100, 50, 255, 0.1));
        color: #00ffc8;
        border-color: rgba(0, 255, 200, 0.6);
        box-shadow: 0 0 20px rgba(0, 255, 200, 0.15);
        transform: translateY(-2px);
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.2), rgba(100, 50, 255, 0.15));
        color: #00ffc8;
        border-color: rgba(0, 255, 200, 0.8);
        box-shadow: 0 0 30px rgba(0, 255, 200, 0.3), inset 0 0 20px rgba(0, 255, 200, 0.1);
        transform: translateY(-2px);
    }

    [data-testid="stTabPanel"] {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.5), rgba(45, 27, 78, 0.3));
        border: 1.5px solid rgba(0, 255, 200, 0.2);
        border-radius: 0 12px 12px 12px;
        padding: 2rem;
        backdrop-filter: blur(15px);
        box-shadow: inset 0 0 30px rgba(100, 50, 255, 0.05);
    }

    .upload-area {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.1) 0%, rgba(155, 89, 182, 0.1) 100%);
        border: 2px dashed rgba(52, 152, 219, 0.4);
        border-radius: 15px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .upload-area:hover {
        border-color: rgba(52, 152, 219, 0.8);
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.15) 0%, rgba(155, 89, 182, 0.15) 100%);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.15);
    }

    .btn-primary {
        background: linear-gradient(135deg, #00ffc8 0%, #6432ff 50%, #ff0096 100%);
        color: #0a0e27;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 25px rgba(0, 255, 200, 0.3);
        width: 100%;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }

    .btn-primary::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }

    .btn-primary:hover {
        background: linear-gradient(135deg, #00ffc8 0%, #6432ff 50%, #ff0096 100%);
        box-shadow: 0 10px 40px rgba(0, 255, 200, 0.5), inset 0 0 20px rgba(255, 255, 255, 0.1);
        transform: translateY(-3px);
    }

    .btn-primary:hover::before {
        left: 100%;
    }

    .claim-box {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.05), rgba(100, 50, 255, 0.05));
        border-left: 4px solid #00ffc8;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 200, 0.2);
        transition: all 0.3s ease;
    }

    .claim-box:hover {
        box-shadow: 0 8px 25px rgba(0, 255, 200, 0.15);
        border-color: rgba(0, 255, 200, 0.4);
    }

    .claim-box.verified {
        border-left-color: #00ff88;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.08), rgba(0, 255, 136, 0.04));
        border-color: rgba(0, 255, 136, 0.2);
    }

    .claim-box.verified:hover {
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
        border-left-color: #00ff88;
    }

    .claim-box.inaccurate {
        border-left-color: #ffaa00;
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.08), rgba(255, 170, 0, 0.04));
        border-color: rgba(255, 170, 0, 0.2);
    }

    .claim-box.inaccurate:hover {
        box-shadow: 0 8px 25px rgba(255, 170, 0, 0.2);
        border-left-color: #ffaa00;
    }

    .claim-box.false {
        border-left-color: #ff3366;
        background: linear-gradient(135deg, rgba(255, 51, 102, 0.08), rgba(255, 51, 102, 0.04));
        border-color: rgba(255, 51, 102, 0.2);
    }

    .claim-box.false:hover {
        box-shadow: 0 8px 25px rgba(255, 51, 102, 0.2);
        border-left-color: #ff3366;
    }

    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
        backdrop-filter: blur(10px);
        text-transform: uppercase;
        font-size: 0.8rem;
    }

    .status-verified {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 255, 136, 0.1));
        color: #00ff88;
        border: 1.5px solid rgba(0, 255, 136, 0.6);
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
    }

    .status-inaccurate {
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.2), rgba(255, 170, 0, 0.1));
        color: #ffaa00;
        border: 1.5px solid rgba(255, 170, 0, 0.6);
        box-shadow: 0 0 15px rgba(255, 170, 0, 0.2);
    }

    .status-false {
        background: linear-gradient(135deg, rgba(255, 51, 102, 0.2), rgba(255, 51, 102, 0.1));
        color: #ff3366;
        border: 1.5px solid rgba(255, 51, 102, 0.6);
        box-shadow: 0 0 15px rgba(255, 51, 102, 0.2);
    }

    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.1), rgba(100, 50, 255, 0.08));
        border: 1.5px solid rgba(0, 255, 200, 0.4);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0, 255, 200, 0.15), inset 0 0 20px rgba(100, 50, 255, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        border-color: rgba(0, 255, 200, 0.8);
        box-shadow: 0 12px 48px rgba(0, 255, 200, 0.25), inset 0 0 30px rgba(100, 50, 255, 0.1);
        transform: translateY(-5px);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffc8 0%, #6432ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(0, 255, 200, 0.3);
    }

    .metric-label {
        font-size: 0.9rem;
        color: rgba(0, 255, 200, 0.8);
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .success-message {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 255, 136, 0.05));
        border: 1.5px solid rgba(0, 255, 136, 0.4);
        color: #00ff88;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: inset 0 0 15px rgba(0, 255, 136, 0.05);
    }

    .info-box {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.12), rgba(100, 50, 255, 0.08));
        border: 1.5px solid rgba(0, 255, 200, 0.3);
        color: rgba(0, 255, 200, 0.95);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: inset 0 0 20px rgba(0, 255, 200, 0.05);
    }

    h2 {
        color: #00d4ff;
        margin-bottom: 1.5rem;
        font-size: 1.8rem;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
    }

    h3 {
        color: rgba(200, 200, 200, 0.95);
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    p, span {
        color: rgba(200, 200, 200, 0.85);
        line-height: 1.6;
    }

    .claim-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: #e8e8e8;
        margin-bottom: 0.8rem;
    }

    .claim-detail {
        margin: 0.5rem 0;
        padding: 0.5rem 0;
    }

    .claim-detail strong {
        color: rgba(200, 200, 200, 0.95);
        display: block;
        margin-bottom: 0.3rem;
        font-size: 0.9rem;
    }

    .claim-detail span {
        color: #00d4ff;
        font-weight: 600;
    }

    a {
        color: #3498db;
        text-decoration: none;
        transition: all 0.2s ease;
    }

    a:hover {
        color: #00d4ff;
        text-decoration: underline;
    }

    .progress-text {
        color: #00d4ff;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
    }

</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False
    if "extraction_done" not in st.session_state:
        st.session_state.extraction_done = False
    if "verification_done" not in st.session_state:
        st.session_state.verification_done = False
    if "claims" not in st.session_state:
        st.session_state.claims = []
    if "results" not in st.session_state:
        st.session_state.results = []
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = ""


def get_status_class(status: str) -> str:
    if status == "VERIFIED":
        return "verified"
    elif status == "INACCURATE":
        return "inaccurate"
    else:
        return "false"


def get_status_badge(status: str) -> str:
    class_name = get_status_class(status)
    icon = "✓" if status == "VERIFIED" else ("⚠" if status == "INACCURATE" else "✗")
    return f'<span class="status-badge status-{class_name}">{icon} {status}</span>'


def main():
    init_session_state()

    st.markdown("""
    <div class="header-container">
        <h1>🔍 FACT CHECKER AI</h1>
        <p>Automated Claim Verification Against Live Web Data</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 UPLOAD & EXTRACT", "✓ VERIFY CLAIMS", "📊 RESULTS"])

    with tab1:
        st.markdown("<h2>Step 1: Upload PDF Document</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            pdf_file = st.file_uploader(
                "Drag and drop or click to upload PDF",
                type=["pdf"],
                key="pdf_uploader",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        if pdf_file is not None:
            st.session_state.pdf_uploaded = True
            st.markdown(f'<div class="success-message">✓ Uploaded: <strong>{pdf_file.name}</strong></div>', unsafe_allow_html=True)

            if st.button("🔍 EXTRACT CLAIMS", key="extract_btn", use_container_width=True):
                with st.spinner("🔄 Extracting claims from PDF..."):
                    try:
                        pdf_text, page_count = PDFProcessor.extract_text_from_pdf(pdf_file)
                        st.session_state.pdf_text = pdf_text

                        extractor = ClaimExtractor()
                        st.session_state.claims = extractor.extract_claims(pdf_text)
                        st.session_state.extraction_done = True

                        st.markdown(f'<div class="success-message">✓ Extracted <strong>{len(st.session_state.claims)}</strong> claims from <strong>{page_count}</strong> pages</div>', unsafe_allow_html=True)

                        if st.session_state.claims:
                            with st.expander("📋 View Extracted Claims"):
                                for i, claim in enumerate(st.session_state.claims, 1):
                                    st.markdown(f"""
                                    <div class="claim-box">
                                        <div class="claim-text">{i}. {claim.text}</div>
                                        <div class="claim-detail"><strong>Type:</strong> <span>{claim.claim_type}</span></div>
                                        <div class="claim-detail"><strong>Confidence:</strong> <span>{claim.extraction_confidence:.0%}</span></div>
                                    </div>
                                    """, unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    with tab2:
        if st.session_state.extraction_done:
            st.markdown("<h2>Step 2: Verify Claims Against Live Web Data</h2>", unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">Ready to verify <strong>{len(st.session_state.claims)}</strong> claims. This may take 1-2 minutes.</div>', unsafe_allow_html=True)

            if st.button("⚡ START VERIFICATION", key="verify_btn", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_placeholder = st.empty()

                fact_checker = FactChecker()
                all_results = []

                for idx, claim in enumerate(st.session_state.claims, 1):
                    status_text.markdown(f'<p class="progress-text">Verifying claim {idx}/{len(st.session_state.claims)}...</p>', unsafe_allow_html=True)
                    progress_bar.progress(idx / len(st.session_state.claims))

                    try:
                        result = fact_checker.verify_claim(claim)
                        all_results.append(result)

                        with results_placeholder.container():
                            status_html = get_status_badge(result.status)
                            st.markdown(f"""
                            <div class="claim-box {get_status_class(result.status)}">
                                <div class="claim-text">Claim: {claim.text}</div>
                                {status_html}
                                <div class="claim-detail"><strong>Correct Value:</strong> <span>{result.correct_value}</span></div>
                                <div class="claim-detail"><strong>Source:</strong> <span><a href="{result.source_url}" target="_blank">{result.source_url[:60]}...</a></span></div>
                                <div class="claim-detail"><strong>Confidence:</strong> <span>{result.confidence_score:.0%}</span></div>
                            </div>
                            """, unsafe_allow_html=True)

                    except Exception as e:
                        st.warning(f"⚠ Error verifying claim {idx}: {str(e)}")

                st.session_state.results = all_results
                st.session_state.verification_done = True
                progress_bar.progress(1.0)
                status_text.markdown('<p class="progress-text">✓ Verification Complete!</p>', unsafe_allow_html=True)

        else:
            st.markdown('<div class="info-box">👈 First extract claims from the PDF (Step 1)</div>', unsafe_allow_html=True)

    with tab3:
        if st.session_state.verification_done and st.session_state.results:
            st.markdown("<h2>Verification Results Dashboard</h2>", unsafe_allow_html=True)

            verified_count = sum(1 for r in st.session_state.results if r.status == "VERIFIED")
            inaccurate_count = sum(1 for r in st.session_state.results if r.status == "INACCURATE")
            false_count = sum(1 for r in st.session_state.results if r.status == "FALSE")
            avg_confidence = sum(r.confidence_score for r in st.session_state.results) / len(st.session_state.results) if st.session_state.results else 0

            st.markdown(f"""
            <div class="metrics-container">
                <div class="metric-card">
                    <div class="metric-label">✓ VERIFIED</div>
                    <div class="metric-value">{verified_count}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">⚠ INACCURATE</div>
                    <div class="metric-value">{inaccurate_count}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">✗ FALSE</div>
                    <div class="metric-value">{false_count}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">📊 CONFIDENCE</div>
                    <div class="metric-value">{avg_confidence:.0%}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            results_data = []
            for result in st.session_state.results:
                results_data.append({
                    "Claim": result.original_claim[:60],
                    "Status": result.status,
                    "Correct Value": result.correct_value[:40],
                    "Confidence": f"{result.confidence_score:.0%}",
                })

            df = pd.DataFrame(results_data)

            st.markdown("""
            <style>
                .results-table {
                    font-size: 0.9rem;
                    margin: 1.5rem 0;
                }
                .stDataFrame {
                    background: linear-gradient(135deg, rgba(0, 255, 200, 0.05), rgba(100, 50, 255, 0.05)) !important;
                    border: 1px solid rgba(0, 255, 200, 0.2) !important;
                    border-radius: 10px !important;
                    backdrop-filter: blur(10px) !important;
                }
            </style>
            """, unsafe_allow_html=True)

            st.dataframe(df, use_container_width=True, hide_index=True)

            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("<p style='color: rgba(0, 255, 200, 0.8); font-size: 0.9rem;'>↑ View full details by hovering over claims above ↑</p>", unsafe_allow_html=True)
            
            with col2:
                csv_buffer = BytesIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()

                st.download_button(
                    label="📥 Export CSV",
                    data=csv_data,
                    file_name=f"fact_check_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        else:
            st.markdown('<div class="info-box">👈 Complete Steps 1 and 2 to see results</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()