import streamlit as st
import time

st.set_page_config(page_title="Admin - AI Fake News Detection", page_icon="⚙️")

st.title("Admin - AI Fake News Detection")

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state.admin_logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials. Please try again.")

else:
    st.subheader("Admin Dashboard")
    st.markdown("Welcome, Admin! Here you can manage system settings and view detailed analytics.")

    st.markdown("### System Settings")
    st.checkbox("Enable Advanced AI Model", value=False)
    st.checkbox("Enable Email Notifications", value=False)
    st.checkbox("Enable Auto-Update", value=True)

    st.markdown("---")
    st.markdown("### Analytics")
    st.write("Loading analytics...")
    time.sleep(2)  # Simulate loading time
    st.write("Total Scans: 1500")
    st.write("Fake News Detected: 450")
    st.write("Real News Detected: 1050")
    st.write("Average Confidence Score: 0.78")