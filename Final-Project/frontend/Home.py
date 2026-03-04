import streamlit as st
import requests

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TruthScanner AI",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)

API = "http://localhost:8000"

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
[data-testid="stAppViewContainer"] { background: #f7f8fc; }
[data-testid="stSidebar"] { background: #1e1e2e; }
[data-testid="stSidebar"] * { color: #cdd6f4 !important; }

/* Force visible text for Streamlit native elements */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] .stMarkdown p { color: #1e1e2e !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1e1e2e 0%, #313244 100%);
    border-radius: 16px;
    padding: 48px 40px;
    color: #cdd6f4;
    margin-bottom: 24px;
}
.hero h1 { font-size: 2.6rem; margin: 0 0 8px; color: #cba6f7; }
.hero p  { font-size: 1.1rem; margin: 0; opacity: .85; }

/* ── Feature cards ── */
.feat-card {
    background: #fff;
    border-radius: 14px;
    padding: 24px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,.07);
    height: 100%;
    border-top: 4px solid #cba6f7;
    transition: transform .15s;
}
.feat-card:hover { transform: translateY(-3px); }
.feat-card h4 { margin: 8px 0 6px; font-size: 1.05rem; color: #1e1e2e; }
.feat-card p  { font-size: .9rem; color: #555; margin: 0; }
.feat-icon    { font-size: 1.8rem; }

/* ── Stat pills ── */
.stat-pill {
    background: #fff;
    border-radius: 12px;
    padding: 18px 24px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,.06);
}
.stat-pill .val { font-size: 2rem; font-weight: 700; color: #cba6f7; }
.stat-pill .lbl { font-size: .82rem; color: #888; margin-top: 2px; }

/* ── How-it-works steps ── */
.step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 18px;
}
.step-num {
    background: #cba6f7;
    color: #1e1e2e;
    border-radius: 50%;
    width: 34px; height: 34px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; flex-shrink: 0;
}
.step-body h5 { margin: 0 0 3px; font-size: .95rem; color: #1e1e2e; }
.step-body p  { margin: 0; font-size: .85rem; color: #666; }

/* ── Status badge ── */
.badge-online  { color: #a6e3a1; font-weight: 600; }
.badge-offline { color: #f38ba8; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🕵️ TruthScanner AI</h1>
  <p>Next-generation misinformation detection — paste text, drop a URL, or scan trending headlines in real time.</p>
</div>
""", unsafe_allow_html=True)

# ─── Live stats row ─────────────────────────────────────────────────────────
stats = None
backend_up = False
try:
    r = requests.get(f"{API}/stats", timeout=2)
    if r.status_code == 200:
        stats = r.json()
        backend_up = True
except Exception:
    pass

sc1, sc2, sc3, sc4, sc5 = st.columns(5)

def stat_pill(col, val, label):
    col.markdown(f"""
    <div class="stat-pill">
      <div class="val">{val}</div>
      <div class="lbl">{label}</div>
    </div>""", unsafe_allow_html=True)

if stats:
    fake_pct = (stats["fake_count"] / stats["total_scans"] * 100) if stats["total_scans"] else 0
    stat_pill(sc1, stats["total_scans"], "Articles Scanned")
    stat_pill(sc2, stats["fake_count"],  "Fake Detected")
    stat_pill(sc3, stats["real_count"],  "Real Verified")
    stat_pill(sc4, f"{stats['avg_confidence']:.0%}", "Avg. Confidence")
    stat_pill(sc5, f"{fake_pct:.1f}%",  "Fake Rate")
else:
    for col, (v, l) in zip(
        [sc1, sc2, sc3, sc4, sc5],
        [("—","Articles Scanned"),("—","Fake Detected"),("—","Real Verified"),("—","Avg. Confidence"),("—","Fake Rate")]
    ):
        stat_pill(col, v, l)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Feature cards ──────────────────────────────────────────────────────────
st.markdown("### 🔧 What TruthScanner AI Can Do")
c1, c2, c3, c4 = st.columns(4)

cards = [
    ("🔗", "URL Scraping",        "Paste any news URL and we'll extract and analyse the article automatically."),
    ("📡", "Trending Headlines",   "Pull live RSS feeds from BBC, Reuters, NPR and more — scan them in one click."),
    ("📊", "Deep Analysis",        "Sentiment, subjectivity, top keywords, credibility score & flagged patterns."),
    ("📅", "Full History",         "Every scan is stored. Filter, search and export your analysis history as CSV."),
]
for col, (icon, title, desc) in zip([c1, c2, c3, c4], cards):
    col.markdown(f"""
    <div class="feat-card">
      <div class="feat-icon">{icon}</div>
      <h4>{title}</h4>
      <p>{desc}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── How it works ───────────────────────────────────────────────────────────
left, right = st.columns([1.1, 1])

with left:
    st.markdown("### ⚙️ How It Works")
    steps = [
        ("Input",    "Paste article text directly, provide a URL to scrape, or pick a trending headline."),
        ("Analyse",  "The heuristic engine checks sentiment, subjectivity, keyword patterns and more."),
        ("Verdict",  "Each article receives a Real / Fake verdict plus a 0–100% credibility score."),
        ("Feedback", "You can flag inaccurate results to help improve the model over time."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="step">
          <div class="step-num">{i}</div>
          <div class="step-body"><h5>{title}</h5><p>{desc}</p></div>
        </div>""", unsafe_allow_html=True)

with right:
    st.markdown("### 🖥️ System Status")
    status_icon = "🟢" if backend_up else "🔴"
    status_word = "Online"  if backend_up else "Offline"
    badge_cls   = "badge-online" if backend_up else "badge-offline"
    st.markdown(f"""
    <div style="background:#fff;border-radius:14px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,.06);">
      <table style="width:100%;border-collapse:collapse;font-size:.92rem;">
        <tr><td style="padding:8px 0;color:#666;">Backend API</td>
            <td style="text-align:right"><span class="{badge_cls}">{status_icon} {status_word}</span></td></tr>
        <tr><td style="padding:8px 0;color:#666;">AI Engine</td>
            <td style="text-align:right"><span class="badge-online">🟢 Heuristic v2</span></td></tr>
        <tr><td style="padding:8px 0;color:#666;">Database</td>
            <td style="text-align:right"><span class="badge-online">🟢 SQLite</span></td></tr>
        <tr><td style="padding:8px 0;color:#666;">Web Scraper</td>
            <td style="text-align:right"><span class="badge-online">🟢 BeautifulSoup4</span></td></tr>
        <tr><td style="padding:8px 0;color:#666;">RSS Feeds</td>
            <td style="text-align:right"><span class="badge-online">🟢 feedparser</span></td></tr>
        <tr><td style="padding:8px 0;color:#666;">API Version</td>
            <td style="text-align:right;color:#888;">v2.0</td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

    if not backend_up:
        st.warning("Backend is offline. Start it with `python run.py` from the project root.", icon="⚠️")
    else:
        st.success("All systems operational. Navigate to **Analyze** to get started!", icon="✅")

