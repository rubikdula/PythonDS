import streamlit as st
def calculate(num1, num2, operation):
    if operation == "Add":
        return num1 + num2
    elif operation == "Subtract":
        return num1 - num2
    elif operation == "Multiply":
        return num1 * num2
    elif operation == "Divide":
        try:
            result = num1 / num2
        except ZeroDivisionError as e:
            result = "Cannot divide by zero."
        return result

def main():
    st.title("Calculator")
    num1 = st.number_input("Enter first number", step=1)
    num2 = st.number_input("Enter second number", step=1)
    operation = st.radio("Select operation", ["Add", "Subtract", "Multiply", "Divide"])
    result = calculate(num1, num2, operation)

    st.write(f"Result of the {operation} of {num1} and {num2} is: {result}")

if __name__ == '__main__':
    main()