import sqlite3
from models import Movie, MovieCreate

def create_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect('movies.db')
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    """Create the movies table if it doesn't exist."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        director TEXT NOT NULL
    );
    ''')
    connection.commit()
    connection.close()

create_table()

def create_movie(movie: MovieCreate) -> int:
    """Adds a new movie to the database
        Args:
        movie (MovieCreate): Movie data to be added
        Returns:
        int: ID of the newly created movie
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO movies (title, director) VALUES (?, ?)',
        (movie.title, movie.director)
    )
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return movie_id

def read_movie():
    """Fetches all movies from the database
        Returns:
        List[Movie]: List of all movies in the database
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies')
    rows = cursor.fetchall()
    movies = [Movie(id=row[0], title=row[1], director=row[2]) for row in rows]
    return movies
def read_movie_by_id(movie_id: int) -> Movie | None:
    """Fetches a movie by its ID
        Args:
        movie_id (int): ID of the movie to fetch
        Returns:
        Movie | None: Movie object if found, else None
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Movie(id=row["id"], title=row["title"], director=row["director"])

def update_movie(movie_id: int, movie: MovieCreate) -> bool:
    """Updates an existing movie in the database
        Args:
        movie_id (int): ID of the movie to update
        movie (MovieCreate): Updated movie data
        Returns:
        bool: True if the movie was updated, False otherwise
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE movies SET title = ?, director = ? WHERE id = ?',
        (movie.title, movie.director, movie_id)
    )
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0

def delete_movie(movie_id: int) -> bool:
    """Deletes a movie from the database
        Args:
        movie_id (int): ID of the movie to delete
        Returns:
        bool: True if the movie was deleted, False otherwise
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0