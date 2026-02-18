import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Global Statistics")


def get_stats():
    try:
        response = requests.get("http://localhost:8000/stats")
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None


stats = get_stats()

if stats:
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Articles Scanned", stats['total_scans'])
    col2.metric("Fake News Detected", stats['fake_count'], delta_color="inverse")
    col3.metric("Real News Verified", stats['real_count'])
    col4.metric("Avg. Confidence AI", f"{stats['avg_confidence']:.2%}")

    st.markdown("---")

    # Charts
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Real vs Fake Distribution")
        data = {
            "Type": ["Real", "Fake"],
            "Count": [stats['real_count'], stats['fake_count']]
        }
        fig = px.pie(data, values='Count', names='Type', color='Type',
                     color_discrete_map={'Real': 'green', 'Fake': 'red'})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("System Performance")
        st.markdown("Simulated backend load and response distribution.")
        # Mock data for the chart since backend doesn't track time
        mock_data = pd.DataFrame({
            "Time": pd.date_range("2023-01-01", periods=10),
            "Requests": [5, 12, 4, 15, 20, 8, 10, 15, 18, 22]
        })
        st.line_chart(mock_data.set_index("Time"))

else:
    st.error("Could not fetch statistics from backend.")