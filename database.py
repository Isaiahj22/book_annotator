import sqlite3
from pathlib import Path

DB_PATH = Path("data/annotations.db")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            quote TEXT,
            thoughts TEXT,
            location TEXT,
            created_at TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    conn.commit()
    conn.close()

def add_book(title, author):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    conn.commit()
    conn.close()


def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, author FROM books")
    books = cursor.fetchall()

    conn.close()
    return books

def get_annotations_for_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, quote, created_at
        FROM annotations
        WHERE book_id = ?
        ORDER BY created_at DESC
        """,
        (book_id,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows

