import streamlit as st

st.sidebar.header("Sidebar")
st.sidebar.write("This is the sidebar area.")
st.sidebar.selectbox("Select an option from the sidebar", ["Option A", "Option B", "Option C"])
st.sidebar.radio("Choose an option", ["Choice 1", "Choice 2", "Choice 3"])