import streamlit as st
import requests
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import os

from rsa.key import gen_keys

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

api_key_input = st.text_input("Enter your API Key:", type="password")
def validate_api_key(api_key):
    headers = {"API-Key": api_key}
    response = requests.get(f"{BASE_URL}/api/api_key/", headers=headers)
    return response.status_code == 200


def dashboard_author(api_key):
    st.title("Book Author")
    st.subheader("Book Author")
    authors = get_authors()
    df_authors = pd.DataFrame(authors)
    st.dataframe(df_authors, use_container_width=True)

    st.subheader("add new author")
    new_author_name = st.text_input("Author Name")

    if st.button("Add Author"):
        if new_author_name.strip():
            add_author(api_key, new_author_name)
        else:
            st.error("Author name cannot be empty.")

    action = st.radio("Select Action", ("Update Author", "Delete Author"))

    if action == "Update Author":
        selected_author = st.selectbox("Select Author to Update", options=[author['name'] for author in authors])
        new_author_name = st.text_input("Author Name", value=selected_author)

        if st.button("Update Author"):
            author_id = next((author['id'] for author in authors if author['name'] == selected_author), None)
            update_author(api_key, author_id, new_author_name)

    elif action == "Delete Author":
        author_to_delete = st.text_input("Author to Delete",options=[author['name'] for author in authors])
        if st.button("Delete Author"):
            author_id = next((author['id'] for author in authors if author['name'] == author_to_delete), None)
            delete_author(api_key, author_id)

st.subheader("Existing Books")
books = get_books()
author = get_authors()

author_id_to_name = {a['id']: a['name'] for a in author}

for book in books:
    book ['author']
    book['author_name'] = author_id_to_name.get(book['author'], "Unknown Author")
    book['genres'] = ','.join(book['genres'])
    del book['author_id']

df_books = pd.DataFrame(books)
st.dataframe(df_books, use_container_width=True)
selected_author = st.selectbox("Select Author", options=[author['name'] for author in author], key="selected_author_add")
new_book_average = st.number_input("New Book Average", min_value=0.0, max_value=5.0, step=0.1)
new_book_genres = st.text_input('Genres (comma separated)')
new_book_year = st.number_input("New Book Year", min_value=1440, max_value=datetime.now().year, step=1)

if st.button("Add Book"):
    if selected_author.strip() and new_book_title.strip():
        genres_list = [genre.strip( ) for genre in new_book_genres.split(',') if genre.strip()]
        selected_author_id = next((a['id'] for a in author if a['name'] == selected_author), None)

        book_data = {
            "title": new_book_title,
            "author": selected_author_id,
            "book_link": "",
            "average_rating": new_book_average,
            "published": new_book_year,
            "genres": genres_list
        }
        add_book(api_key, book_data)
    else:
        st.error("Book title and author cannot be empty.")

action = st.radio("Select Action",options=["Update Book", "Delete Book"], key="book_action")

if action == "Update Book":
    selected_book = st.selectbox('Select Book to Update', options=[book['title'] for book in books], key="selected_book_update")

    if selected_book:
        book = next ((book for book in books if book['title'] == selected_book), None)
        new_book_title = st.text_input("Book Title", value=book['title'])
        selected_author_name = st.selectbox("Select Author", options=[author['name'] for author in author], index=next((i for i, a in enumerate(author) if a['id'] == book['author']), 0), key="selected_author_update")
        new_book_average = st.number_input("New Book Average", min_value=0.0, max_value=5.0, step=0.1, value=book['average_rating'])
        new_book_genres = st.text_input('Genres (comma separated)', value=book['genres'])
        new_book_year = st.number_input("New Book Year", min_value=1440, max_value=datetime.now().year, step=1, value=book['published'])
        book_id = book['id']

        if st.button("Update Books"):
            genres_list = [g.strip() for g in new_book_genres.split(',') if g.strip()]
            book_data = {
                "title": new_book_title,
                "author": next((a['id'] for a in author if a['name'] == selected_author_name), None),
                "book_link": book.get['book_link'],
                "average_rating": new_book_average,
                "published": new_book_year,
                "genres": genres_list
            }
            update_book(api_key, book_id, book_data)

elif action == "Delete Book":
    book_to_delete = st.text_input("Book to Delete", options=[book['title'] for book in books], key="selected_book_delete")
    if st.button("Delete Book"):
        book_id = next((book['id'] for book in books if book['title'] == book_to_delete), None)
        delete_book(api_key, book_id)

def visualization_dashboard():
    st.title("Book Visualization")
    book = get_books()
    author = get_authors()

    df_books = pd.DataFrame(books)

    if 'author_id' in df_books.columns:
        author_id_to_name = {a['id']: a['name'] for a in author}
        df_books['author_name'] = df_books['author_id'].map(author_id_to_name)
        df_books.drop(columns=['author_id'], inplace=True)

    st.sidebar.title("Filters")
    selected_author = st.sidebar.multiselect("Select Author", options=df_books["All"] + list(author_id_to_name.values())
    )

    min_year = int(df_books['published'].min())
    max_year = int(df_books['published'].max())
    selected_year_range = st.sidebar.slider("Select Publication Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))
    selected_rating_range = st.sidebar.slider("Select Average Rating Range", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1),

    filters_applied = selected_author !="All" or selected_year_range != (min_year, max_year) or selected_rating_range != (0.0, 5.0)

    if st.sidebar.button("Filter") or not filters_applied:
        filtered_books = df_books.copy()

        if selected_author and "All" not in selected_author:
            filtered_books = filtered_books[filtered_books['author_name'].isin(selected_author)]

        filtered_books = filtered_books[
            (filtered_books['published'] >= selected_year_range[0]) &
            (filtered_books['published'] <= selected_year_range[1]) &
            (filtered_books['average_rating'] >= selected_rating_range[0]) &
            (filtered_books['average_rating'] <= selected_rating_range[1])
        ]

        st.subheader("Filtered Books")
        st.dataframe(filtered_books, use_container_width=True)

        if not filters_book.empty:
            st.subheader("Books by Year")
            books_by_year = filtered_books.groupby('published').size().reset_index(name='count')
            fig_year = px.bar(books_by_year, x='published', y='count', title="Number of Books Published Each Year")
            st.plotly_chart(fig_year, use_container_width=True)
            fig_years.update_traces(texttemplate='%{y}s', textposition='inside')
            fig_years.update_layout(
                informtext_minsize = 8,
                uniformtext_minsize = 8,
                uniformtext_mode = 'hide',
                xaxis_title=dict(tickmode='linear', tick0=min_year, dtick=5, tickangel=-45, tickfront=dict(size=10)),
                yaxis_title=dict(title='Number of Books Published Each Year', range(0, books_by_year['count'].max() + 1)),
                title_x=0.5
            ),
            st.plotly_chart(fig_years, use_container_width=True)

            st.subheader("Books by Genre")
            books_by_rating = filtered_books.groupby('average_rating').size().reset_index(name='count')
            fig_rating = px.bar(books_by_rating, x='average_rating', y='count', title="Number of Books Average Rating", labels={'average_rating': 'Average Rating'})
            fig_rating.update_traces(texttemplate='%{y}', textposition='inside')
            fig_rating.update_layout(informtext_minsize = 8, uniformtext_minsize = 8, uniformtext_mode = 'hide')
            st.plotly_chart(fig_rating, use_container_width=True)
        else:
            st.warning("Please select at least one author")
    else:
        st.warning("Please select at least one filter or click the Filter button to see results.")

st.sidebar.title("navigation")
option = st.sidebar.selectbox("Select Dashboard", ("Author Management", "Book Visualization"))
if option == "Vizualization Dashboard":
    visualization_dashboard()
if api_key_input and validate_api_key(api_key_input):
    if option == "Author Management":
        dashboard_author(api_key_input)
else:    st.warning("Please enter a valid API key to access the dashboard.")