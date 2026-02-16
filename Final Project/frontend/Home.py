import streamlit as st

st.set_page_config(
    page_title="AI Fake News Detection",
    page_icon="📰",
    layout="wide",
)

st.title("AI Fake News Detection Platform")
st.markdown("Welcome to the AI Fake News Detection Platform! This tool is designed to help you identify and analyze")

col1, col2 = st.columns(2)

with col1:
    st.image("https://c.files.bbci.co.uk/7BE9/production/_99712713_gettyimages-639620990.jpg", caption="Uncover the truth behind the headlines with our AI-powered fake news detection tool.")

with col2:
    st.markdown("""Fight Misinformation with AI! Our platform uses advanced algorithms to analyze news articles and social media posts, helping you distinguish between real and fake news. Stay informed and make smarter decisions with our easy-to-use interface.
    
        ### Modules Available:
        -**Analyze**: Paste text to get and instant real/fake breakdown.
        -**Dashboard**: View global statistics of scanned articles.
        -**History**: Browse the complete archive of all checks
        -**Admin**: Manage system settings.
        
    Select a page from the sidebar to get started    
    
    """)

    st.info("Note: This platform is for educational purposes only and should not be used as the sole source of information for critical decisions. Always verify news from multiple sources.")

st.markdown("---")
st.markdown("##### System Status")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Backend Status", "Operational", "v1.0.0")
col_b.metric("Database", "SQLite3", "Connected")
col_c.metric("Model", "Heuristic Engine", "Alpha")

