import streamlit as st

with st.container(border=True):
    st.header("This is a container")
    st.write("Containers help group related elements together.")

st.write("Outside the container now.")