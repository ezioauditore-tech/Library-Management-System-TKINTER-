import json
import sqlite3

# Read data from JSON file
with open('books.json',encoding='utf-8') as file:
    data = json.load(file)

# Connect to SQLite database
conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS book")

# Create a table if it doesn't exist
cursor.execute('CREATE TABLE IF NOT EXISTS Book (Id INTEGER PRIMARY KEY, Title TEXT, Authors TEXT, ISBN TEXT, language TEXT, publication TEXT,available INTEGER )')

# Iterate over the data and insert into the table
for book in data:
    book_id = int(book['bookID'])
    title = str(book['title'])
    author = str(book['authors'])
    isbn = book['isbn']
    language = book['language_code']
    publication_year = book['publication_date']
    cursor.execute('INSERT INTO Book (Id, Title, Authors, ISBN, language, publication) VALUES (?, ?, ?, ?, ?, ?)', (book_id, title, author, isbn, language, publication_year))

# Commit the changes and close the connection
cursor.execute("UPDATE book SET available = (ABS(RANDOM()) % 5) + 1")
conn.commit()
conn.close()
