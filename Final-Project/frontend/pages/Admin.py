import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Admin · TruthScanner", page_icon="⚙️", layout="wide")

API = "http://localhost:8000"

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f7f8fc; }
[data-testid="stSidebar"] { background: #1e1e2e; }
[data-testid="stSidebar"] * { color: #cdd6f4 !important; }

/* Force text visibility in light theme overrides */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] .stMarkdown { color: #1e1e2e !important; }

.kpi-card {
    background:#fff; border-radius:14px; padding:22px 18px;
    box-shadow:0 2px 8px rgba(0,0,0,.06); text-align:center;
}
.kpi-val { font-size:2rem; font-weight:700; color:#cba6f7; }
.kpi-lbl { font-size:.82rem; color:#888; margin-top:3px; }
</style>
""", unsafe_allow_html=True)

# ─── Auth gate ───────────────────────────────────────────────────────────────
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<h1 style='color:#1e1e2e;'>⚙️ Admin Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                if username == "admin" and password == "password":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    st.stop()

# ─── Admin panel ─────────────────────────────────────────────────────────────
st.markdown("<h1 style='color:#1e1e2e;'>⚙️ Admin Control Panel</h1>", unsafe_allow_html=True)
st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.update({"admin_logged_in": False}))

# ─── Live KPIs ───────────────────────────────────────────────────────────────
try:
    r = requests.get(f"{API}/stats", timeout=3)
    stats = r.json() if r.status_code == 200 else None
except Exception:
    stats = None

if stats:
    k1, k2, k3, k4, k5 = st.columns(5)
    for col, val, lbl in [
        (k1, stats["total_scans"],              "Total Scans"),
        (k2, stats["fake_count"],               "Fake Detected"),
        (k3, stats["real_count"],               "Real Verified"),
        (k4, f"{stats['avg_confidence']:.1%}",  "Avg. Confidence"),
        (k5, stats.get("feedback_count", 0),    "Feedback Entries"),
    ]:
        col.markdown(f'<div class="kpi-card"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)
else:
    st.warning("Could not reach the backend API.")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ────────────────────────────────────────────────────────────────────
tab_analytics, tab_feedback, tab_settings = st.tabs(["📊 Analytics", "💬 User Feedback", "🔧 Settings"])

# ── Analytics tab ─────────────────────────────────────────────────────────
with tab_analytics:
    try:
        r2 = requests.get(f"{API}/history?limit=200", timeout=3)
        history = r2.json() if r2.status_code == 200 else []
    except Exception:
        history = []

    if history:
        df = pd.DataFrame(history)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Verdict Distribution")
            vc = df["verdict"].value_counts().reset_index()
            vc.columns = ["Verdict", "Count"]
            fig = px.pie(vc, values="Count", names="Verdict",
                         color="Verdict",
                         color_discrete_map={"Real": "#a6e3a1", "Fake": "#f38ba8"},
                         hole=0.4)
            fig.update_layout(margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Confidence Score Distribution")
            fig2 = px.histogram(df, x="confidence_score", color="verdict",
                                color_discrete_map={"Real": "#a6e3a1", "Fake": "#f38ba8"},
                                nbins=20, barmode="overlay", opacity=0.75)
            fig2.update_layout(margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No article data available yet.")

# ── Feedback tab ──────────────────────────────────────────────────────────
with tab_feedback:
    try:
        r3 = requests.get(f"{API}/feedback/all", timeout=3)
        feedback_data = r3.json() if r3.status_code == 200 else []
    except Exception:
        feedback_data = []

    if feedback_data:
        fdf = pd.DataFrame(feedback_data)
        st.dataframe(
            fdf,
            column_config={
                "id":            "ID",
                "article_id":    "Article ID",
                "title":         "Article Title",
                "user_feedback": "Feedback",
                "timestamp":     "Submitted At",
            },
            use_container_width=True,
            hide_index=True,
        )
        correct   = len(fdf[fdf["user_feedback"] == "correct"])
        incorrect = len(fdf[fdf["user_feedback"] == "incorrect"])
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Feedback", len(fdf))
        m2.metric("Marked Correct",   correct)
        m3.metric("Marked Incorrect", incorrect)
    else:
        st.info("No feedback submitted yet.")

# ── Settings tab ──────────────────────────────────────────────────────────
with tab_settings:
    st.subheader("Model Settings")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.toggle("Enable Advanced Heuristics", value=True)
        st.toggle("Save Scraped Articles",       value=True)
        st.toggle("Maintenance Mode",            value=False)
    with col_s2:
        st.slider("Fake Detection Sensitivity", 0.0, 1.0, 0.5,
                  help="Higher = more articles flagged as fake")
        st.slider("Max Scrape Length (chars)",  1000, 15000, 10000, step=500)

    st.info("These settings are for display purposes in this prototype. In production they would be persisted.")

