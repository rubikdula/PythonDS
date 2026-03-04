import streamlit as st

st.set_page_config(page_title="About · TruthScanner", page_icon="ℹ️", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f7f8fc; }
[data-testid="stSidebar"] { background: #1e1e2e; }
[data-testid="stSidebar"] * { color: #cdd6f4 !important; }

/* Force main content text colours regardless of Streamlit theme */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] .stMarkdown p,
[data-testid="stAppViewContainer"] .stMarkdown li { color: #1e1e2e !important; }

.section-card {
    background: #fff;
    border-radius: 14px;
    padding: 28px 28px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07);
    margin-bottom: 20px;
    color: #1e1e2e;
}
.section-card h3  { color: #1e1e2e; margin: 0 0 12px; font-size: 1.15rem; }
.section-card p   { color: #555; font-size: .92rem; line-height: 1.6; margin: 0 0 8px; }
.section-card ol  { color: #444; padding-left: 20px; font-size: .92rem; line-height: 1.8; }
.section-card ul  { color: #444; padding-left: 20px; font-size: .92rem; line-height: 1.8; }
.section-card li  { margin-bottom: 4px; }
.section-card em  { color: #888; }
.tech-badge {
    display: inline-block;
    background: #f0eeff;
    color: #6c4ead;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: .85rem;
    font-weight: 600;
    margin: 3px;
}
</style>
""", unsafe_allow_html=True)

st.title("ℹ️ About TruthScanner AI")

left, right = st.columns([1.3, 1])

with left:
    st.markdown("""
    <div class="section-card">
      <h3>🛡️ What Is TruthScanner AI?</h3>
      <p>TruthScanner AI is a full-stack misinformation-detection prototype that combines
      heuristic natural-language analysis, live web scraping, and RSS feed monitoring to
      help users evaluate the credibility of news articles.</p>
      <p>It was built as a learning project to demonstrate how Python back-end services
      (FastAPI) and interactive front-ends (Streamlit) can be combined with real-world
      data sources like live news feeds.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
      <h3>⚙️ How the Analysis Works</h3>
      <ol>
        <li><b>Linguistic analysis</b> — TextBlob computes sentiment polarity and subjectivity.</li>
        <li><b>Keyword heuristics</b> — The engine scans for sensationalist or emotionally-charged phrases.</li>
        <li><b>Structural checks</b> — ALL-CAPS usage, excessive punctuation and very short texts are flagged.</li>
        <li><b>Credibility markers</b> — References to official sources, studies and data reduce the fake score.</li>
        <li><b>Word-count weighting</b> — Articles with very few words receive a higher suspicion penalty.</li>
        <li><b>Verdict</b> — Scores below 0.25 → Real; above 0.5 → Fake; in-between → probabilistic.</li>
      </ol>
      <p style="font-size:.85rem;color:#888;margin-top:14px;">
        ⚠️ This is a <em>heuristic prototype</em>, not a trained ML model.
        A production system would use a fine-tuned transformer (e.g., BERT) on a labelled dataset.
      </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="section-card">
      <h3>🧰 Tech Stack</h3>
    """, unsafe_allow_html=True)

    tech = {
        "Frontend":    ["Streamlit", "Plotly", "Pandas"],
        "Backend":     ["FastAPI", "Uvicorn", "Pydantic"],
        "AI / NLP":    ["TextBlob", "NLTK"],
        "Scraping":    ["BeautifulSoup4", "feedparser", "requests"],
        "Database":    ["SQLite3"],
    }
    for category, items in tech.items():
        badges = "".join(f'<span class="tech-badge">{t}</span>' for t in items)
        st.markdown(f"<p><b>{category}:</b><br>{badges}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
      <h3>🚀 Features</h3>
      <ul>
        <li>✏️ Paste-text analysis</li>
        <li>🔗 URL article scraping</li>
        <li>📡 Live trending headlines (BBC, Reuters, NPR…)</li>
        <li>📊 Full analytics dashboard</li>
        <li>📚 Searchable & exportable history</li>
        <li>💬 User feedback loop</li>
        <li>🔐 Admin control panel</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
  <h3>👤 Developer</h3>
  <p><b>Name:</b> Rubik Dula &nbsp;|&nbsp; <b>Project:</b> TruthScanner AI &nbsp;|&nbsp; <b>Platform:</b> Python / Streamlit / FastAPI</p>
</div>
""", unsafe_allow_html=True)
