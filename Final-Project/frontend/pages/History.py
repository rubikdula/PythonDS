import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="History · TruthScanner", page_icon="📚", layout="wide")

API = "http://localhost:8000"

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f7f8fc; }
[data-testid="stSidebar"] { background: #1e1e2e; }
[data-testid="stSidebar"] * { color: #cdd6f4 !important; }
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] .stMarkdown p { color: #1e1e2e !important; }
</style>
""", unsafe_allow_html=True)

st.title("📚 Analysis History")

# ─── Fetch ────────────────────────────────────────────────────────────────────
def get_history():
    """Fetch history from backend without caching so new scans appear instantly."""
    try:
        r = requests.get(f"{API}/history?limit=500", timeout=5)
        if r.status_code == 200:
            return r.json()
        st.error(f"Backend returned {r.status_code} while loading history.")
        return []
    except Exception as e:
        st.error(f"Could not reach backend at {API}/history: {e}")
        return []

data = get_history()

if not data:
    st.info("No history found. Analyse some articles first!")
    st.stop()

df = pd.DataFrame(data)

# ─── Sidebar filters ──────────────────────────────────────────────────────────
st.sidebar.header("🔎 Filters")
verdict_filter = st.sidebar.multiselect("Verdict", ["Real", "Fake"], default=["Real", "Fake"])
sentiment_opts = df["sentiment"].dropna().unique().tolist() if "sentiment" in df.columns else []
sentiment_filter = st.sidebar.multiselect("Sentiment", sentiment_opts, default=sentiment_opts)
search_term = st.sidebar.text_input("Search in title / content", "")

# ─── Apply filters ────────────────────────────────────────────────────────────
filtered = df[df["verdict"].isin(verdict_filter)]
if sentiment_filter and "sentiment" in filtered.columns:
    filtered = filtered[filtered["sentiment"].isin(sentiment_filter)]
if search_term:
    mask = (
        filtered["title"].str.contains(search_term, case=False, na=False)
        | filtered["content"].str.contains(search_term, case=False, na=False)
    )
    filtered = filtered[mask]

# ─── Stats bar ───────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.metric("Showing",       len(filtered))
c2.metric("Fake in view",  len(filtered[filtered["verdict"] == "Fake"]))
c3.metric("Real in view",  len(filtered[filtered["verdict"] == "Real"]))

st.divider()

# ─── Table ────────────────────────────────────────────────────────────────────
display_cols = ["id", "title", "verdict", "confidence_score", "sentiment",
                "subjectivity", "word_count", "created_at"]
display_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(
    filtered[display_cols],
    column_config={
        "id":               st.column_config.NumberColumn("ID", width="small"),
        "title":            st.column_config.TextColumn("Title"),
        "verdict":          st.column_config.TextColumn("Verdict"),
        "confidence_score": st.column_config.ProgressColumn("Confidence", format="%.0%", min_value=0, max_value=1),
        "sentiment":        st.column_config.TextColumn("Sentiment"),
        "subjectivity":     st.column_config.TextColumn("Subjectivity"),
        "word_count":       st.column_config.NumberColumn("Words"),
        "created_at":       st.column_config.TextColumn("Scanned At"),
    },
    hide_index=True,
    use_container_width=True,
)

# ─── Detail expander ─────────────────────────────────────────────────────────
st.markdown("#### 📄 View Full Article")
if not filtered.empty:
    selected_id = st.selectbox(
        "Select article ID",
        filtered["id"].tolist(),
        format_func=lambda x: f"#{x} — {filtered[filtered['id']==x]['title'].values[0][:60]}"
    )
    row = filtered[filtered["id"] == selected_id].iloc[0]
    with st.expander("Full Content", expanded=True):
        col_a, col_b = st.columns(2)
        col_a.markdown(f"**Title:** {row['title']}")
        col_a.markdown(f"**Author:** {row.get('author','—')}")
        col_a.markdown(f"**Source URL:** {row.get('source_url','—') or '—'}")
        col_b.markdown(f"**Verdict:** {'🔴 FAKE' if row['verdict']=='Fake' else '🟢 REAL'}")
        col_b.markdown(f"**Confidence:** {row['confidence_score']:.1%}")
        col_b.markdown(f"**Scanned:** {row.get('created_at', '—')}")
        st.text_area("Article Body", row.get("content",""), height=220, disabled=True)

# ─── Export ───────────────────────────────────────────────────────────────────
st.divider()
st.download_button(
    "⬇️ Download filtered results as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="truthscanner_history.csv",
    mime="text/csv",
    use_container_width=True,
)

