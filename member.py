from tkinter import *
from book import Book
from libData import LibData
from tkinter import messagebox
from datetime import datetime


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
        search = Toplevel(self.window)
        search.title("search results")
        search.geometry("500x400")
        scrollbar = Scrollbar(search)
        scrollbar.pack(side="right", fill="y")
        search_results_listbox = Listbox(search, width=500, height=400, yscrollcommand=scrollbar.set)
        search_results_listbox.pack()
        scrollbar.config(command=search_results_listbox.yview)
        data = self.search_entry.get()
        result = LibData.searchBook(data)
        search_results_listbox.delete(0, "end")
        book_list = "ISBN - Title - Authors\n"
        i = 1
        for book in result:
            book_list= f"{i} - {book[2]} - {book[0]} - {book[1]}"
            i += 1
            search_results_listbox.insert("end", book_list)

        search.mainloop()

    def getBorrowedBook(self):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
              SELECT book.isbn, book.title, borrow.borrowDate
              FROM book, borrow
              WHERE borrow.bookId = book.Id
              AND borrow.userId = :uId
              AND borrow.status = :status
              """, {'uId': self.Id, 'status': 'borrowed'})

        books = c.fetchall()
        print(books)

        if not books:
            messagebox.showinfo('Borrowed Books','You have not borrowed any book yet!')
        else:
            borrow=Toplevel(self.window)
            borrow.title("Borrowed Books")
            borrow.geometry("500x400")
            scrollbar = Scrollbar(borrow)
            scrollbar.pack(side="right", fill="y")
            borrow_listbox = Listbox(borrow, width=500, height=400, yscrollcommand=scrollbar.set)
            borrow_listbox.pack()
            scrollbar.config(command=borrow_listbox.yview)
            i = 1
            for book in books:
                book_info = f"{i} -- {book[0]} -- {book[1]} --{book[2]}"
                i+=1
                borrow_listbox.insert("end", book)

            borrow.mainloop()
            for book in books:
                print(f"{book[0]} - {book[1]}")
            print('')

        conn.commit()
        conn.close()

    def run(self):
        self.window.mainloop()


