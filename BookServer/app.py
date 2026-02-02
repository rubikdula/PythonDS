import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

api_key_input = st.text_input("Enter your API Key:", type="password")

def validate_api_key(api_key):
    headers = {"API-Key": api_key}
    response = requests.get(f"{BASE_URL}/api/api_key/", headers=headers)
    return response.status_code == 200

def get_authors():
    response = requests.get(f"{BASE_URL}/api/authors/")
    return response.json() if response.status_code == 200 else None

def add_author(api_key, name):
    headers = {"API-Key": api_key}
    data = {"name": name}
    response = requests.post(f"{BASE_URL}/api/authors/", headers=headers, json=data)
    return response.status_code == 200

def update_author(api_key, author_id, name):
    headers = {"API-Key": api_key}
    data = {"name": name}
    response = requests.put(f"{BASE_URL}/api/authors/{author_id}", headers=headers, json=data)
    return response.status_code == 200

def delete_author(api_key, author_id):
    headers = {"API-Key": api_key}
    response = requests.delete(f"{BASE_URL}/api/authors/{author_id}", headers=headers)
    return response.status_code == 200

def get_books():
    response = requests.get(f"{BASE_URL}/api/books/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch books.")
        return []

def add_book(api_key, book_data):
    headers = {"API-Key": api_key}
    response = requests.post(f"{BASE_URL}/api/books/", headers=headers, json=book_data)
    if response.status_code == 200:
        st.success("Book added successfully.")
    else:
        st.error("Failed to add book.")

def update_book(api_key, book_id, book_data):
    headers = {"API-Key": api_key}
    response = requests.put(f"{BASE_URL}/api/books/{book_id}", headers=headers, json=book_data)
    if response.status_code == 200:
        st.success("Book updated successfully.")
    else:
        st.error("Failed to update book.")

def delete_book(api_key, book_id):
    headers = {"API-Key": api_key}
    response = requests.delete(f"{BASE_URL}/api/books/{book_id}", headers=headers)
    if response.status_code == 200:
        st.success("Book deleted successfully.")
    else:
        st.error("Failed to delete book.")