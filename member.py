from tkinter import *
from book import Book
from libData import LibData


class Memebr:

    def __init__(self, Id):
        self.Id = Id
        self.window = Tk()
        self.window.title("Library Management System - Member")
        self.window.geometry("500x400")

        # create input fields and labels
        self.isbn_label = Label(self.window, text="ISBN:")
        self.isbn_label.pack()
        self.isbn_entry = Entry(self.window)
        self.isbn_entry.pack()

        # create buttons
        self.borrow_button = Button(self.window, text="Borrow", command=self.borrow)
        self.borrow_button.pack()

        self.reserve_button = Button(self.window, text="Reserve", command=self.reserve)
        self.reserve_button.pack()

        self.return_button = Button(self.window, text="Return", command=self.return_book)
        self.return_button.pack()

        self.fine_button = Button(self.window, text="Calculate Fine", command=self.fine)
        self.fine_button.pack()

        self.search_label = Label(self.window, text="Search:")
        self.search_label.pack()
        self.search_entry = Entry(self.window)
        self.search_entry.pack()

        self.search_button = Button(self.window, text="Search", command=self.searchBook)
        self.search_button.pack()

        self.borrowed_button = Button(self.window, text="List of Borrowed Books", command=self.getBorrowedBook)
        self.borrowed_button.pack()

        self.quit_button = Button(self.window, text="Quit", command=self.window.destroy)
        self.quit_button.pack()

    def borrow(self):
        isbn = self.isbn_entry.get()
        bookId = Book.getBookIdByIsbn(isbn)
        LibData.borrowBook(self.Id, bookId)

    def reserve(self):
        isbn = self.isbn_entry.get()
        bookId = Book.getBookIdByIsbn(isbn)
        LibData.reserveBook(self.Id, bookId)

    def return_book(self):
        isbn = self.isbn_entry.get()
        bookId = Book.getBookIdByIsbn(isbn)
        LibData.returnBook(bookId)

    def fine(self):
        userId = self.Id
        isbn = self.isbn_entry.get()
        bookId = Book.getBookIdByIsbn(isbn)
        LibData.calculateFine(userId, bookId)

    def searchBook(self):
        data = self.search_entry.get()
        LibData.searchBook(data)

    def getBorrowedBook(self):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                  select book.isbn,book.title from book,borrow
                  where borrow.bookId = book.Id
                  and borrow.userId = :uId and borrow.status = :status
                  """, {'uId': self.Id, 'status': 'borrowed'})

        books = c.fetchall()
        print(books)

        if not books:
            print('You have not borrowed any book yet!')
            print('')
        else:
            print('')
            print('*********************')
            print('* List Of Borowed Book*')
            print('*********************')
            for book in books:
                print(f"{book[0]} - {book[1]}")
            print('')

        conn.commit()
        conn.close()

    def run(self):
        self.window.mainloop()


