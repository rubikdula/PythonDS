import streamlit as st
import requests

st.set_page_config(page_title="Trending · TruthScanner", page_icon="📡", layout="wide")

API = "http://localhost:8000"

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f7f8fc; }
[data-testid="stSidebar"] { background: #1e1e2e; }
[data-testid="stSidebar"] * { color: #cdd6f4 !important; }
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] .stMarkdown p,
[data-testid="stAppViewContainer"] .stCaption { color: #1e1e2e !important; }

.news-card {
    background: #fff;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,.06);
    border-left: 4px solid #cba6f7;
    transition: box-shadow .15s;
}
.news-card:hover { box-shadow: 0 4px 14px rgba(0,0,0,.10); }
.news-card h5   { margin: 0 0 6px; font-size: .98rem; color: #1e1e2e; }
.news-card p    { margin: 0; font-size: .83rem; color: #666; }
.news-meta      { font-size: .76rem; color: #aaa; margin-top: 6px; }

.verdict-fake { color: #f38ba8; font-weight: 700; }
.verdict-real { color: #a6e3a1; font-weight: 700; }
.verdict-pend { color: #b8b8b8; font-weight: 400; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ─── Session ──────────────────────────────────────────────────────────────────
if "trending_results" not in st.session_state:
    st.session_state.trending_results = {}  # {link: analysis_result}


# ─── Helpers ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def fetch_sources():
    try:
        r = requests.get(f"{API}/trending/sources", timeout=3)
        return r.json().get("sources", []) if r.status_code == 200 else []
    except Exception:
        return []


@st.cache_data(ttl=120, show_spinner=False)
def fetch_headlines(source: str, max_items: int):
    try:
        r = requests.get(f"{API}/trending", params={"source": source, "max_items": max_items}, timeout=10)
        return r.json().get("items", []) if r.status_code == 200 else []
    except Exception:
        return []


def analyse_headline(item: dict):
    """Send headline summary to /predict and return result."""
    text = (item.get("summary") or "") + " " + item.get("title", "")
    if len(text.strip()) < 20:
        return None
    try:
        r = requests.post(
            f"{API}/predict",
            json={"text": text, "title": item["title"], "author": item.get("source", "RSS")},
            timeout=10,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


# ─── UI ───────────────────────────────────────────────────────────────────────
st.title("📡 Trending News Scanner")
st.caption("Pull live headlines from major RSS feeds and analyse them for credibility in one click.")

# Sidebar controls
st.sidebar.header("📡 Feed Settings")
sources = fetch_sources()
if not sources:
    sources = ["BBC News", "Reuters", "NPR News", "Al Jazeera", "The Guardian"]

selected_source = st.sidebar.selectbox("News Source", sources)
max_items       = st.sidebar.slider("Max Headlines", 5, 20, 10)
st.sidebar.divider()
auto_analyse    = st.sidebar.toggle("Auto-analyse on load", value=False)

# Fetch button
col_btn, col_clear = st.columns([3, 1])
with col_btn:
    do_fetch = st.button("🔄 Fetch Latest Headlines", type="primary", use_container_width=True)
with col_clear:
    if st.button("🗑️ Clear Results", use_container_width=True):
        st.session_state.trending_results = {}
        st.cache_data.clear()

headlines = fetch_headlines(selected_source, max_items)

if not headlines and not do_fetch:
    st.info("Click **Fetch Latest Headlines** to load live news from the RSS feed.")
    st.stop()

if not headlines:
    st.error("Could not fetch headlines. The backend may be offline or the RSS feed may be unavailable.")
    st.stop()

st.markdown(f"Showing **{len(headlines)}** headlines from **{selected_source}**")
st.divider()

# ─── Batch-analyse button ────────────────────────────────────────────────────
if st.button("⚡ Analyse All Headlines", use_container_width=True):
    progress = st.progress(0, text="Analysing…")
    for i, item in enumerate(headlines):
        key = item["link"]
        if key not in st.session_state.trending_results:
            result = analyse_headline(item)
            if result:
                st.session_state.trending_results[key] = result
        progress.progress((i + 1) / len(headlines), text=f"Analysing {i+1}/{len(headlines)}…")
    progress.empty()
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─── Headline cards ───────────────────────────────────────────────────────────
for item in headlines:
    key    = item["link"]
    result = st.session_state.trending_results.get(key)

    if result:
        verdict = result["verdict"]
        conf    = result["confidence"]
        verdict_html = (
            f'<span class="verdict-fake">🚨 FAKE ({conf:.0%})</span>' if verdict == "Fake"
            else f'<span class="verdict-real">✅ REAL ({conf:.0%})</span>'
        )

        border_color = "#f38ba8" if verdict == "Fake" else "#a6e3a1"
        extra_style  = f"border-left-color:{border_color};"
    else:
        verdict_html = '<span class="verdict-pend">Not yet analysed</span>'
        extra_style  = ""

    # Card
    title   = item.get("title", "No Title")
    summary = item.get("summary", "")[:160]
    pub     = item.get("published", "")
    link    = item.get("link", "#")

    st.markdown(f"""
    <div class="news-card" style="{extra_style}">
      <h5>{title}</h5>
      <p>{summary}{"…" if len(item.get("summary","")) > 160 else ""}</p>
      <div class="news-meta">
        {verdict_html} &nbsp;·&nbsp;
        <a href="{link}" target="_blank" style="color:#89b4fa;text-decoration:none;">🔗 Read original</a>
        &nbsp;·&nbsp; {pub}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not result:
        btn_col, _ = st.columns([1, 4])
        if btn_col.button(f"Analyse", key=f"btn_{key}", use_container_width=True):
            with st.spinner("Analysing…"):
                r = analyse_headline(item)
                if r:
                    st.session_state.trending_results[key] = r
                    st.rerun()
                else:
                    st.error("Could not analyse this headline.")

    # Expandable detail if analysed
    if result:
        with st.expander("View flags & keywords"):
            flags     = result.get("flags", [])
            top_words = result.get("top_words", {})
            sent      = result.get("sentiment","—")
            subj      = result.get("subjectivity","—")
            m1, m2, m3 = st.columns(3)
            m1.metric("Sentiment",    sent)
            m2.metric("Subjectivity", subj)
            m3.metric("Credibility",  f"{result.get('credibility_score',0):.0%}")
            if flags:
                for f in flags:
                    colour = "🟢" if f.startswith("✅") else "🟠"
                    st.markdown(f"{colour} {f}")
            if top_words:
                st.markdown(f"**Top words:** {', '.join(top_words.keys())}")
