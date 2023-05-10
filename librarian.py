from book import Book
from libData import LibData
import tkinter as tk
from tkinter import messagebox


class Librarian:

    def __init__(self, Id):
        self.Id = Id
        self.window = tk()
        self.window.title("Library Management System - Member")
        self.window.geometry("500x400")

    def updateBook(self):
        isbn = self.inputBox('Please enter isbn of book that you want to update:')
        bookId = Book.getBookIdByIsbn(isbn)
        if bookId is None:
            self.messageBox('Error', 'Book with the provided ISBN not found.')
            return
        title = self.inputBox('Please enter the new title:')
        authors = self.inputBox('Please enter the new authors:')
        Book.updateBook(bookId, title, authors)
        self.messageBox('Success', 'Book details updated successfully.')

    def viewBorrowedBooks(self):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                  select book.isbn,book.title from book,borrow
                  where borrow.bookId = book.Id
                  and borrow.status = :status
                  """, {'uId': self.Id, 'status': 'borrowed'})

        books = c.fetchall()
        if not books:
            self.messageBox('No borrowed books', 'No borrowed books found.')
        else:
            book_list = "\n".join([f"{book[0]} - {book[1]}" for book in books])
            self.messageBox('List of Borrowed Books', book_list)

        conn.commit()
        conn.close()

    def searchBook(self):
        data = self.inputBox('Please enter search data:')
        search_results = LibData.searchBook(data)
        if not search_results:
            self.messageBox('Search Results', 'No books found matching the search criteria.')
        else:
            book_list = "\n".join([f"{book['isbn']} - {book['title']}" for book in search_results])
            self.messageBox('Search Results', book_list)

    def getBorrowedBookforUser(self):
        pass

    def menu(self):
        root = tk.Tk()
        root.geometry('400x300')
        root.title('Library Management System')
        
        title_label = tk.Label(root, text='Welcome Librarian', font=('Arial', 16))
        title_label.pack(pady=10)
        
        update_button = tk.Button(root, text='Update Books', command=self.updateBook)
        update_button.pack(pady=5)

        view_borrowed_button = tk.Button(root, text='View All Borrowed Books', command=self.viewBorrowedBooks)
        view_borrowed_button.pack(pady=5)

        search_button = tk.Button(root, text='Search Books', command=self.searchBook)
        search_button.pack(pady=5)

        quit_button = tk.Button(root, text='Quit', command=root.destroy)
        quit_button.pack(pady=5)

        root.mainloop()

    def inputBox(self, message):
        return messagebox.askquestion('Input', message)

    def messageBox(self, title, message):
        messagebox.showinfo(title, message)

    def foo(self):
        pass
