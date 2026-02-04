import streamlit as st
import requests
from dotenv import load_dotenv
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