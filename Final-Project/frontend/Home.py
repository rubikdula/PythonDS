import streamlit as st

st.set_page_config(
    page_title="AI Fake News Platform",
    page_icon="🕵️",
    layout="wide"
)

st.title("🕵️ AI Fake News Platform")
st.markdown("### Welcome to the Advanced Fake News Detection System")

col1, col2 = st.columns(2)

with col1:
    st.image("https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=2070&auto=format&fit=crop",
             caption="Uncover the Truth")

with col2:
    st.markdown("""
    **Fight Misinformation with AI**

    This platform leverages rudimentary heuristic algorithms (prototype methodology) to analyze news articles and determine their veracity.

    ### Modules available:

    - **🔍 Analyze**: Paste text to get an instant real/fake breakdown.
    - **📊 Dashboard**: View global statistics of scanned articles.
    - **📚 History**: Browse the complete archive of all checks.
    - **⚙️ Admin**: Manage system settings (Mock).

    Select a page from the sidebar to get started.
    """)

    st.info("💡 Tip: Navigate using the sidebar menu on the left.")

st.markdown("---")
st.markdown("##### System Status")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Backend", "Online", "v1.0.0")
col_b.metric("Model", "Heuristic Engine", "Alpha")
col_c.metric("Database", "SQLite3", "Connected")
