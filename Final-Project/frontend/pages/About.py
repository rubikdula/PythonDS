import streamlit as st

st.set_page_config(page_title="About - AI Fake News Detection", page_icon="ℹ️")

st.title("About - AI Fake News Detection")

st.markdown("""
###AI Fake News Detection Platform

This platform is a demonstration of a simple AI-powered fake news detection system. It is designed to analyze news articles and social media posts to help users identify potential misinformation.

###Tech Stack:
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: SQLite3
- **AI Model**: Heuristic-based pattern matching (for demonstration purposes)
- **Data Vizualisation**: Plotly, Pandas

### How "AI" Works:
For this prototype, the "AI" is a heuristic engine that uses simple rules and randomization to classify text as "Fake" or "Real". In a production system, this would be replaced with a trained machine learning model.
It checks for:
- Presence of certain keywords often associated with fake news.
- Randomized patterns to simulate complex analysis.
- Confidence scores are generated to provide insight into the model's certainty.

### Developer:
- **Name**: Rubik Dula

""")