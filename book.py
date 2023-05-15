import sqlite3

class Book:
    
    @staticmethod
    def addBook(title, authors, isbn):
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        # Insert a new book into the database
        c.execute("""
            INSERT INTO Book (title, authors, isbn)
            VALUES (:title, :authors, :isbn)
        """, {'title': title, 'authors': authors, 'isbn': isbn})
        
        conn.commit()
        conn.close()
        print("Book added successfully!")
    
    def deleteBook(bookId):
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        # Delete the book from the database based on the book ID
        c.execute("""
            DELETE FROM Book
            WHERE id = :bookId
        """, {'bookId': bookId})
        
        conn.commit()
        conn.close()
        print("Book deleted successfully!")
    
    @staticmethod
    def updateBook(bookId, title, authors):
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        # Update the book with the given bookId
        c.execute("""
            UPDATE Book
            SET title = :title, authors = :authors
            WHERE id = :bookId
        """, {'title': title, 'authors': authors, 'bookId': bookId})
        
        conn.commit()
        conn.close()
        print("Book updated successfully!")
    
    @staticmethod
    def checkAvailability(bookId):
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        # Retrieve the availability of the book with the given bookId
        c.execute("""
            SELECT available
            FROM Book
            WHERE id = :bookId
        """, {'bookId': bookId})
        
        availability = c.fetchone()[0]
        
        conn.close()
        return availability
    @staticmethod
    def getBookIdByIsbn(isbn):
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        # Retrieve the book ID based on the given ISBN
        c.execute("""
            SELECT id
            FROM Book
            WHERE isbn = :isbn
        """, {'isbn': isbn})
        
        result = c.fetchone()
        
        conn.close()
        
        if result:
            print(result[0])
            return result[0]  # Return the book ID
        else:
            return None
    @staticmethod
    def updateAvailability(number, bookId):
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        # Update the availability of the book with the given bookId
        c.execute("""
            UPDATE Book
            SET available = :number
            WHERE id = :bookId
        """, {'number': number, 'bookId': bookId})
        
        conn.commit()
        conn.close()
