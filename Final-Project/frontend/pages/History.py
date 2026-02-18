import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="History", page_icon="📚", layout="wide")

st.title("📚 Analysis History")


def get_history():
    try:
        response = requests.get("http://localhost:8000/history")
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []


data = get_history()

if data:
    df = pd.DataFrame(data)

    # Filters
    st.sidebar.header("Filters")
    verdict_filter = st.sidebar.multiselect("Filter by Verdict", ["Real", "Fake"], default=["Real", "Fake"])

    if not df.empty:
        filtered_df = df[df['verdict'].isin(verdict_filter)]

        st.dataframe(
            filtered_df,
            column_config={
                "id": "ID",
                "title": "Headline",
                "verdict": st.column_config.TextColumn("Verdict", help="AI Decision"),
                "confidence_score": st.column_config.ProgressColumn("Confidence", format="%.2f", min_value=0,
                                                                    max_value=1),
                "author": "Author",
                "content": "Content Snippet"
            },
            hide_index=True,
            use_container_width=True
        )

        st.download_button(
            "Download CSV",
            data=filtered_df.to_csv().encode('utf-8'),
            file_name="fake_news_history.csv",
            mime="text/csv"
        )
else:
    st.info("No history found in database.")
