import streamlit as st

with st.form("My_form", clear_on_submit=True):
    st.header("User Information Form")

    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, max_value=120)
    email = st.text_input("Enter your email")
    biography = st.text_area("Enter your biography")
    terms = st.checkbox("I agree to the terms and conditions")
    submitted = st.form_submit_button(label="Submit")

if submitted:
    st.write(f"Hello, {name}!")
    st.write(f"Age: {age}")
    st.write(f"Email: {email}")
    st.write(f"Biography: {biography}")
    if terms:
        st.write(f"You have agreed to the terms and conditions.")
    else:
        st.write(f"You have not agreed to the terms and conditions.")
