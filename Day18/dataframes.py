import pandas as pd
import streamlit as st

st.header("Displaying DataFrames in Streamlit")

data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [22, 27, 32, 29, 24],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']

})

st.dataframe(data)

st.write("You can also use st.table to display a static table:")

