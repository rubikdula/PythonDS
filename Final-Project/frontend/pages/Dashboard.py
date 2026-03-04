import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard · TruthScanner", page_icon="📊", layout="wide")

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
.kpi-card {
    background:#fff; border-radius:14px; padding:22px 18px;
    box-shadow:0 2px 8px rgba(0,0,0,.06); text-align:center;
}
.kpi-val { font-size:2.2rem; font-weight:700; color:#cba6f7; }
.kpi-lbl { font-size:.82rem; color:#888; margin-top:3px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Analytics Dashboard")

# ─── Fetch data ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def fetch_stats():
    try:
        r = requests.get(f"{API}/stats", timeout=3)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=30)
def fetch_history():
    try:
        r = requests.get(f"{API}/history?limit=200", timeout=3)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []

stats   = fetch_stats()
history = fetch_history()

if not stats:
    st.error("Cannot reach the backend. Make sure the API server is running.")
    st.stop()

# ─── KPI row ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
fake_pct = (stats["fake_count"] / stats["total_scans"] * 100) if stats["total_scans"] else 0

kpis = [
    (k1, stats["total_scans"],            "Total Scans"),
    (k2, stats["fake_count"],             "Fake Detected"),
    (k3, stats["real_count"],             "Real Verified"),
    (k4, f"{stats['avg_confidence']:.1%}", "Avg. Confidence"),
    (k5, stats.get("feedback_count", 0),  "User Feedback"),
]
for col, val, lbl in kpis:
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-val">{val}</div>
      <div class="kpi-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Charts ──────────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("Real vs Fake Distribution")
    pie_data = {"Type": ["Real", "Fake"], "Count": [stats["real_count"], stats["fake_count"]]}
    fig_pie = px.pie(
        pie_data, values="Count", names="Type",
        color="Type",
        color_discrete_map={"Real": "#a6e3a1", "Fake": "#f38ba8"},
        hole=0.45,
    )
    fig_pie.update_traces(textinfo="percent+label", pull=[0, 0.05])
    fig_pie.update_layout(showlegend=False, margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("Credibility Score Distribution")
    if history:
        df = pd.DataFrame(history)
        fig_hist = px.histogram(
            df, x="confidence_score", color="verdict",
            color_discrete_map={"Real": "#a6e3a1", "Fake": "#f38ba8"},
            nbins=20, barmode="overlay", opacity=0.75,
            labels={"confidence_score": "Confidence Score", "verdict": "Verdict"},
        )
        fig_hist.update_layout(margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa")
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("No history data available yet.")

# ─── Sentiment breakdown ──────────────────────────────────────────────────────
if history:
    df = pd.DataFrame(history)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Sentiment Breakdown")
        if "sentiment" in df.columns:
            sent_counts = df["sentiment"].value_counts().reset_index()
            sent_counts.columns = ["Sentiment", "Count"]
            fig_sent = px.bar(
                sent_counts, x="Sentiment", y="Count",
                color="Sentiment",
                color_discrete_map={"Positive": "#a6e3a1", "Negative": "#f38ba8", "Neutral": "#89b4fa"},
                text="Count",
            )
            fig_sent.update_layout(showlegend=False, margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa")
            st.plotly_chart(fig_sent, use_container_width=True)

    with c4:
        st.subheader("Subjectivity Breakdown")
        if "subjectivity" in df.columns:
            subj_counts = df["subjectivity"].value_counts().reset_index()
            subj_counts.columns = ["Subjectivity", "Count"]
            fig_subj = px.pie(
                subj_counts, values="Count", names="Subjectivity",
                color_discrete_sequence=["#cba6f7", "#89b4fa"],
                hole=0.45,
            )
            fig_subj.update_layout(margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_subj, use_container_width=True)

    # ─── Recent scans table ────────────────────────────────────────────
    st.subheader("🗂️ Recent Scans")
    preview_df = df[["title", "verdict", "confidence_score", "sentiment", "word_count", "created_at"]].head(10).copy()
    preview_df.columns = ["Title", "Verdict", "Confidence", "Sentiment", "Words", "Scanned At"]
    st.dataframe(
        preview_df,
        column_config={
            "Confidence": st.column_config.ProgressColumn("Confidence", format="%.0%", min_value=0, max_value=1),
        },
        use_container_width=True,
        hide_index=True,
    )
