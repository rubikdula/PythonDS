import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Analyze · TruthScanner", page_icon="🔍", layout="wide")

API = "http://localhost:8000"

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f7f8fc; }
[data-testid="stSidebar"] { background: #1e1e2e; }
[data-testid="stSidebar"] * { color: #cdd6f4 !important; }
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] .stMarkdown p { color: #1e1e2e !important; }

.result-card {
    background: #fff;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07);
    margin-bottom: 14px;
}
.verdict-fake { color: #f38ba8; font-size: 1.5rem; font-weight: 700; }
.verdict-real { color: #a6e3a1; font-size: 1.5rem; font-weight: 700; }
.flag-item {
    background: #fff5f5;
    border-left: 3px solid #f38ba8;
    padding: 6px 12px;
    border-radius: 0 6px 6px 0;
    margin: 4px 0;
    font-size: .88rem;
    color: #333;
}
.flag-ok {
    background: #f0fff4;
    border-left: 3px solid #a6e3a1;
    padding: 6px 12px;
    border-radius: 0 6px 6px 0;
    margin: 4px 0;
    font-size: .88rem;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# ─── Session state ───────────────────────────────────────────────────────────
for key, default in [
    ("last_result", None),
    ("feedback_submitted", False),
    ("scraped_data", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def submit_feedback(article_id: int, feedback_type: str):
    try:
        requests.post(f"{API}/feedback", json={"article_id": article_id, "user_feedback": feedback_type})
        st.toast("Feedback recorded!", icon="✅")
    except Exception as e:
        st.error(f"Feedback error: {e}")


def confidence_gauge(confidence: float, verdict: str):
    colour = "#f38ba8" if verdict == "Fake" else "#a6e3a1"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(confidence * 100, 1),
        number={"suffix": "%", "font": {"size": 28}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 10}},
            "bar": {"color": colour},
            "bgcolor": "#f0f0f0",
            "steps": [
                {"range": [0,  40], "color": "#fff5f5"},
                {"range": [40, 65], "color": "#fefce8"},
                {"range": [65,100], "color": "#f0fff4"},
            ],
        },
        title={"text": "Confidence", "font": {"size": 14}},
    ))
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10), height=180, paper_bgcolor="rgba(0,0,0,0)")
    return fig


def keyword_bar(top_words: dict):
    if not top_words:
        return None
    df = pd.DataFrame(top_words.items(), columns=["Word", "Count"]).sort_values("Count")
    fig = go.Figure(go.Bar(
        x=df["Count"], y=df["Word"],
        orientation="h",
        marker_color="#cba6f7",
    ))
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#eee"),
    )
    return fig


# ─── Layout ─────────────────────────────────────────────────────────────────
st.title("🔍 Analyze a News Article")

left, right = st.columns([1.05, 1], gap="large")

# ═══════════════════════════════════════════════════════════════════════════
# LEFT — Input panel
# ═══════════════════════════════════════════════════════════════════════════
with left:
    input_tab, url_tab = st.tabs(["✏️  Paste Text", "🔗  Scrape from URL"])

    # ── Tab 1: Paste text ────────────────────────────────────────────────
    with input_tab:
        news_title  = st.text_input("Article Title", placeholder="Optional — helps with record-keeping")
        news_author = st.text_input("Author", value="Anonymous")
        news_text   = st.text_area("Article Content", height=260, placeholder="Paste the full article body here…")

        if st.button("🚀 Analyse Article", type="primary", use_container_width=True):
            if not news_text.strip():
                st.warning("Please enter some text to analyse.")
            else:
                with st.spinner("Running analysis…"):
                    try:
                        payload = {
                            "text":   news_text,
                            "title":  news_title or "User Query",
                            "author": news_author,
                        }
                        r = requests.post(f"{API}/predict", json=payload, timeout=15)
                        if r.status_code == 200:
                            st.session_state.last_result = r.json()
                            st.session_state.feedback_submitted = False
                            if r.json()["verdict"] == "Real":
                                st.balloons()
                            st.rerun()
                        else:
                            st.error(f"Backend error {r.status_code}: {r.text}")
                    except Exception as e:
                        st.error(f"Connection failed: {e}")

    # ── Tab 2: Scrape URL ────────────────────────────────────────────────
    with url_tab:
        url_input = st.text_input("News Article URL", placeholder="https://www.bbc.com/news/…")

        col_fetch, col_analyse = st.columns(2)

        if col_fetch.button("🌐 Fetch Article", use_container_width=True):
            if not url_input.strip():
                st.warning("Please enter a URL.")
            else:
                with st.spinner("Scraping article…"):
                    try:
                        r = requests.post(f"{API}/scrape", json={"url": url_input}, timeout=20)
                        if r.status_code == 200:
                            st.session_state.scraped_data = r.json()
                            st.success("Article fetched! Review below, then click **Analyse**.")
                        else:
                            st.error(f"Scrape failed: {r.json().get('detail','Unknown error')}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

        scraped = st.session_state.scraped_data
        if scraped:
            with st.expander("📄 Scraped Article Preview", expanded=True):
                st.markdown(f"**Title:** {scraped.get('title','—')}")
                st.markdown(f"**Author:** {scraped.get('author','—')} &nbsp; | &nbsp; **Domain:** `{scraped.get('domain','—')}` &nbsp; | &nbsp; **Words:** {scraped.get('word_count',0)}")
                st.text_area("Content Preview", scraped.get("content","")[:800] + "…", height=140, disabled=True)

            if col_analyse.button("🚀 Analyse Scraped Article", type="primary", use_container_width=True):
                with st.spinner("Analysing…"):
                    try:
                        payload = {
                            "text":       scraped.get("content", ""),
                            "title":      scraped.get("title", "Scraped Article"),
                            "author":     scraped.get("author", "Unknown"),
                            "source_url": url_input,
                        }
                        r = requests.post(f"{API}/predict", json=payload, timeout=15)
                        if r.status_code == 200:
                            st.session_state.last_result = r.json()
                            st.session_state.feedback_submitted = False
                            if r.json()["verdict"] == "Real":
                                st.balloons()
                            st.rerun()
                        else:
                            st.error(f"Backend error: {r.text}")
                    except Exception as e:
                        st.error(f"Connection failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# RIGHT — Results panel
# ═══════════════════════════════════════════════════════════════════════════
with right:
    st.markdown("#### 📊 Analysis Results")

    res = st.session_state.last_result

    if not res:
        st.info("Results will appear here after you submit an article.")
    else:
        verdict     = res["verdict"]
        conf        = res["confidence"]
        flags       = res.get("flags", [])
        sentiment   = res.get("sentiment", "Neutral")
        subjectivity = res.get("subjectivity", "Objective")
        top_words   = res.get("top_words", {})
        cred_score  = res.get("credibility_score", 0.5)
        article_id  = res.get("article_id", 0)

        # ── Verdict banner ──────────────────────────────────────────────
        if verdict == "Real":
            st.markdown('<div class="result-card"><span class="verdict-real">✅ REAL</span> — This article appears credible.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card"><span class="verdict-fake">🚨 FAKE</span> — Suspicious content detected.</div>', unsafe_allow_html=True)

        # ── Gauge + credibility ─────────────────────────────────────────
        g1, g2 = st.columns(2)
        g1.plotly_chart(confidence_gauge(conf, verdict), use_container_width=True)
        g2.markdown("<br>", unsafe_allow_html=True)
        g2.metric("Credibility Score", f"{cred_score:.0%}")
        g2.metric("Sentiment",   sentiment)
        g2.metric("Subjectivity", subjectivity)

        # ── Flags ───────────────────────────────────────────────────────
        st.markdown("**Detected Patterns**")
        if flags:
            for f in flags:
                cls = "flag-ok" if f.startswith("✅") else "flag-item"
                st.markdown(f'<div class="{cls}">{f}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="flag-ok">✅ No suspicious patterns detected.</div>', unsafe_allow_html=True)

        # ── Top keywords bar ────────────────────────────────────────────
        if top_words:
            st.markdown("**Top Keywords**")
            fig = keyword_bar(top_words)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

        # ── Feedback ────────────────────────────────────────────────────
        st.divider()
        st.markdown("**Was this verdict accurate?**")
        if not st.session_state.feedback_submitted:
            fb1, fb2 = st.columns(2)
            if fb1.button("👍 Yes, correct", use_container_width=True):
                submit_feedback(article_id, "correct")
                st.session_state.feedback_submitted = True
                st.rerun()
            if fb2.button("👎 No, incorrect", use_container_width=True):
                submit_feedback(article_id, "incorrect")
                st.session_state.feedback_submitted = True
                st.rerun()
        else:
            st.success("Thanks for your feedback!")
