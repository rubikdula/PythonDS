import streamlit as st

def main():
    st.title("Hello, Streamlit!")
    user_input = st.text_input("Enter your name")
    st.write("Your name is", user_input)
    age = st.number_input("Enter your age", min_value=0, max_value=120)
    st.write("Your age is", age)
    st.write("This is a simple Streamlit application.")
    if st.button("Click Me"):
        st.write("Button clicked!")
    if st.checkbox("Show Raw Data"):
        st.write("Here is some raw data")

    message = st.text_area("Enter your message")
    choice = st.radio("Select your option", ["Option 1", "Option 2", "Option 3"])
    st.write("You selected:", choice)
    if st.button("Success"):
        st.success("This is a success message!")

    try:
        1 / 0
    except ZeroDivisionError as e:
        st.error(f"An error occurred: {e}")


if __name__ == '__main__':
    main()