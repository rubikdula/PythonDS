import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

books_df = pd.read_csv('bestsellers_with_categories_2022_03_27.csv')

st.title("Bestselling Books Data Visualization")
st.write("This application visualizes data about bestselling books.")

st.sidebar.header("Add new Book Data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author")
    new_user_rating = st.slider("Rating", 0.0, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("Number of Reviews", min_value=0, step=1)
    new_price = st.number_input("Price", min_value=0.0, value=0.0, step=1.0, format="%.2f")

    new_year = st.number_input("Year", min_value=2009, max_value=2022, step=1)
    new_genre = st.selectbox("Genre", books_df['Genre'].unique())
    submit = st.form_submit_button(label = "Add Book")

if submit:
    new_data = {
        'Name': new_name,
        'Author': new_author,
        'User Rating': new_user_rating,
        'Reviews': new_reviews,
        'Price': new_price,
        'Year': new_year,
        'Genre': new_genre
    }
    books_df = pd.concat([pd.DataFrame(new_data, index=[0]), books_df], ignore_index=True)
    books_df.to_csv('bestsellers_with_categories_2022_03_27.csv', index=False)
    st.sidebar.success("Data Visualization Complete")

#Sidebar filters
st.sidebar.header("Filter Books Data")
selected_author = st.sidebar.selectbox("Select Author", ["All"] + list(books_df['Author'].unique()))
selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(books_df['Year'].unique()))
selected_genre = st.sidebar.selectbox("Select Genre", ["All"] + list(books_df['Genre'].unique()))
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
max_price = st.sidebar.slider("Maximum Price", 0, books_df['Price'].max(), books_df['Price'].max())

#Filter the datasets
filtered_books_df = books_df.copy()
if selected_author != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Author'] == selected_author]
if selected_author != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Author'] == selected_author]
if selected_author != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Author'] == selected_author]

filtered_books_df = filtered_books_df[
    (filtered_books_df['User Rating'] >= min_rating) & (filtered_books_df['Price'] <= max_price)
]
st.subheader("Summary Statistics")
unique_titles = filtered_books_df['Name'].nunique()
average_rating = filtered_books_df['User Rating'].mean()
average_price = filtered_books_df['Price'].mean()
total_reviews = filtered_books_df['Reviews'].sum()
st.write(f"Unique Book Titles: {unique_titles}")
st.write(f"Average User Rating: {average_rating:.2f}")
st.write(f"Total Reviews: {total_reviews}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Rating", average_rating)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Price", f"${average_price:.2f}")
col4.metric("Total Reviews", total_reviews)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Authors")
    top_authors = filtered_books_df['Author'].value_counts().head(10)
    fig_authors = px.bar(top_authors, x=top_authors.index, y=top_authors.values,
                         labels={'x': 'Author', 'y': 'Number of Books'},
                         title="Top 10 Authors by Number of Bestselling Books")
    st.plotly_chart(fig_authors)

with col2:
    st.subheader("Price Distribution")
    fig_price = px.histogram(filtered_books_df, x='Price', nbins=20,
                             labels={'Price': 'Book Price'},
                             title="Distribution of Book Prices")
    st.plotly_chart(fig_price)

st.subheader("Genre Distribution")
fig = px.pie(filtered_books_df, names='Genre', title='Distribution of Book Genres', color='Genre')
color_discrete_sequence = px.colors.sequential.Plasma

st.plotly_chart(fig)

st.subheader("number of Fiction vs Non Fiction Books over Years")
size = filtered_books_df.groupby(['Year', 'Genre']).size().reset_index(name='Counts')
fig = px.bar(size, x='Year', y='Counts', color='Genre', title='Number of Fiction vs Non Fiction Books over Years')
st.plotly_chart(fig)

st.subheader("Top 15 Authors by Counts of Books Published")
top_authors15 = filtered_books_df['Author'].value_counts().head(15).reset_index()
top_authors15.columns = ['Author', 'Counts']
fig = px.bar(top_authors15, x='Counts', y='Author', orientation='h',
             title='Top 15 Authors by Counts of Books Published',
             labels={'Counts': 'Counts of Books Published', 'Author': 'Author'},
             color_discrete_sequence=px.colors.sequential.Viridis)
st.plotly_chart(fig)

st.subheader("Filter Data by Genre")
genre_filter = st.selectbox("Select Genre", options=filtered_books_df['Genre'].unique())
filtered_df = filtered_books_df[filtered_books_df['Genre'] == genre_filter]
st.dataframe(filtered_df)
