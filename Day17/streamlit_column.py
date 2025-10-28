import streamlit as st

col1, col2, col3, col4, col5 = st.columns(5, gap="small", vertical_alignment="center")

with col1:
    st.header("Column 1")
    st.write("This is the first column.")
    if st.button("Button 1"):
        st.write("Button 1 clicked!")

with col2:
    st.header("Column 2")
    st.write("This is the second column.")
    if st.button("Button 2"):
        st.write("Button 2 clicked!")
with col3:
    st.header("Column 3")
    st.write("This is the third column.")
    if st.button("Button 3"):
        st.write("Button 3 clicked!")

with col4:
    st.header("Column 4")
    st.write("This is the fourth column.")
    if st.button("Button 4"):
        st.write("Button 4 clicked!")

with col5:
    st.header("Column 5")
    st.write("This is the fifth column.")
    if st.button("Button 5"):
        st.write("Button 5 clicked!")