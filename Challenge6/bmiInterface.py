import streamlit as st


class BMICalculator:
    def calculate_bmi(weight, height):
        return weight / (height ** 2)

    def get_adult_category(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 24.9:
            return "Normal weight"
        elif bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def get_child_category(bmi):
        if bmi < 14:
            return "Underweight"
        elif bmi < 18:
            return "Normal weight"
        elif bmi < 24:
            return "Overweight"
        else:
            return "Obese"


def main():
    st.title("BMI Calculator")

    # Input fields
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    weight = st.number_input("Weight (kg)", min_value=1.0)
    height = st.number_input("Height (m)", min_value=0.1, max_value=3.0, step=0.01)

    if st.button("Calculate BMI"):
        if name and age > 0 and weight > 0 and height > 0:
            bmi = BMICalculator.calculate_bmi(weight, height)
            category = (BMICalculator.get_adult_category(bmi) if age >= 18
                        else BMICalculator.get_child_category(bmi))

            # Display results
            st.subheader("Results")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {name}")
                st.write(f"**Age:** {age}")
            with col2:
                st.write(f"**BMI:** {bmi:.2f}")
                st.write(f"**Category:** {category}")

            # Add a color-coded indicator
            if category == "Normal weight":
                st.success(f"Your BMI of {bmi:.2f} is in the normal range.")
            elif category == "Underweight":
                st.warning(f"Your BMI of {bmi:.2f} indicates you are underweight.")
            elif category == "Overweight":
                st.warning(f"Your BMI of {bmi:.2f} indicates you are overweight.")
            else:
                st.error(f"Your BMI of {bmi:.2f} indicates obesity.")


if __name__ == "__main__":
    main()
