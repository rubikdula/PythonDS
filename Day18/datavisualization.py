import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

books_df = pd.read_csv('bestsellers_with_categories_2022_03_27.csv')

st.title("Bestselling Books Data Visualization")
st.write("This application visualizes data about bestselling books.")

st.subheader("Summary Statistics")
unique_titles = books_df['Name'].nunique()
average_rating = books_df['User Rating'].mean()
average_price = books_df['Price'].mean()
total_reviews = books_df['Reviews'].sum()
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
    top_authors = books_df['Author'].value_counts().head(10)
    fig_authors = px.bar(top_authors, x=top_authors.index, y=top_authors.values,
                         labels={'x': 'Author', 'y': 'Number of Books'},
                         title="Top 10 Authors by Number of Bestselling Books")
    st.plotly_chart(fig_authors)

with col2:
    st.subheader("Price Distribution")
    fig_price = px.histogram(books_df, x='Price', nbins=20,
                             labels={'Price': 'Book Price'},
                             title="Distribution of Book Prices")
    st.plotly_chart(fig_price)

st.subheader("Genre Distribution")
fig = px.pie(books_df, names='Genre', title='Distribution of Book Genres', color='Genre')
color_discrete_sequence = px.colors.sequential.Plasma

st.plotly_chart(fig)

st.subheader("number of Fiction vs Non Fiction Books over Years")
size = books_df.groupby(['Year', 'Genre']).size().reset_index(name='Counts')
fig = px.bar(size, x='Year', y='Counts', color='Genre', title='Number of Fiction vs Non Fiction Books over Years')
st.plotly_chart(fig)

st.subheader("Top 15 Authors by Counts of Books Published")
top_authors15 = books_df['Author'].value_counts().head(15).reset_index()
top_authors15.columns = ['Author', 'Counts']
fig = px.bar(top_authors15, x='Counts', y='Author', orientation='h',
             title='Top 15 Authors by Counts of Books Published',
             labels={'Counts': 'Counts of Books Published', 'Author': 'Author'},
             color_discrete_sequence=px.colors.sequential.Viridis)
st.plotly_chart(fig)

st.subheader("Filter Data by Genre")
genre_filter = st.selectbox("Select Genre", options=books_df['Genre'].unique())
filtered_df = books_df[books_df['Genre'] == genre_filter]
st.dataframe(filtered_df)
