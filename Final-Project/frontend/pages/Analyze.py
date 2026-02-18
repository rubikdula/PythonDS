import streamlit as st
import requests

st.set_page_config(page_title="Analyze News", page_icon="🔍", layout="wide")

st.title("🔍 Analyze News Article")

# Input Section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input Text")
    news_title = st.text_input("Article Title (Optional)")
    news_author = st.text_input("Author (Optional)", value="Anonymous")
    news_text = st.text_area("Paste Article Content here:", height=300)

    if st.button("Check Veracity", type="primary"):
        if not news_text.strip():
            st.warning("Please enter text to analyze.")
        else:
            with st.spinner("Running Heuristic Engine..."):
                try:
                    payload = {
                        "text": news_text,
                        "title": news_title if news_title else "User Query",
                        "author": news_author
                    }
                    response = requests.post("http://localhost:8000/predict", json=payload)

                    if response.status_code == 200:
                        result = response.json()
                        verdict = result["verdict"]
                        conf = result["confidence"]
                        flags = result.get("flags", [])

                        st.session_state['last_result'] = result
                        st.balloons() if verdict == "Real" else None

                    else:
                        st.error(f"Server returned error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

with col2:
    st.subheader("Analysis Results")

    if 'last_result' in st.session_state:
        res = st.session_state['last_result']
        verdict = res['verdict']
        conf = res['confidence']
        flags = res.get('flags', [])

        if verdict == "Real":
            st.success(f"### Verdict: REAL")
            st.metric("Confidence Score", f"{conf:.1%}", delta="High Trust")
        else:
            st.error(f"### Verdict: FAKE")
            st.metric("Confidence Score", f"{conf:.1%}", delta="-Suspect", delta_color="inverse")

        st.markdown("#### Detected Patterns")
        if flags:
            for flag in flags:
                st.warning(f"⚠️ {flag}")
        else:
            st.info("No suspicious patterns detected.")

    else:
        st.info("Results will appear here after analysis.")

st.markdown("---")
with st.expander("Debugging Info"):
    st.write("Session State:", st.session_state)