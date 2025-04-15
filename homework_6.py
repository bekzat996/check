import sqlite3

class Library:
    def __init__(self, db_name="library.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT
            )
        ''')
        self.connection.commit()

    def add_book(self, title, author):
        self.cursor.execute('''
            INSERT INTO books (title, author) VALUES (?, ?)
        ''', (title, author))
        self.connection.commit()
        print(f"Книга '{title}' добавлена.")

    def delete_book(self, book_id):
        self.cursor.execute('''
            DELETE FROM books WHERE id = ?
        ''', (book_id,))
        self.connection.commit()
        print(f"Книга с ID {book_id} удалена.")

    def list_books(self):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        if books:
            for book in books:
                print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}")
        else:
            print("Библиотека пуста.")

    def __del__(self):
        self.connection.close()
library = Library()

library.add_book("Сынган Кылыч","Тологон Касымбеков")
library.add_book("Манкурт", "Ч. Айтматов")
library.list_books()
library.delete_book(1)
library.list_books()