from book import Book
from libData import LibData
from tkinter import *
from tkinter import messagebox

class Librarian:

    def __init__(self, Id):
        self.Id = Id
        self.window = Tk()
        self.window.title("Library Management System - Librarian")
        self.window.geometry("500x400")

        # create input fields and labels
        self.isbn_label = Label(self.window, text="ISBN:")
        self.isbn_label.pack()
        self.isbn_entry = Entry(self.window)
        self.isbn_entry.pack()
        self.title_label = Label(self.window, text="Title:")
        self.title_label.pack()
        self.title_entry = Entry(self.window)
        self.title_entry.pack()
        self.author_label = Label(self.window, text="Author:")
        self.author_label.pack()
        self.author_entry = Entry(self.window)
        self.author_entry.pack()

        # create buttons
        self.update_button = Button(self.window, text="Update", command=self.updateBook)
        self.update_button.pack()
        # create buttons
        self.add_button = Button(self.window, text="Add", command=self.addBook)
        self.add_button.pack()

        self.isbn_del = Label(self.window, text="Enter ISBN for Deleting:")
        self.isbn_del.pack()
        self.isbn_del_Entry = Entry(self.window)
        self.isbn_del_Entry.pack()
        self.delete_button = Button(self.window, text="Delete", command=self.deleteBook)
        self.delete_button.pack()

        self.borrow_button = Button(self.window, text="Borrowed Books", command=self.viewBorrowedBooks)
        self.borrow_button.pack()


        self.search_label = Label(self.window, text="Search:")
        self.search_label.pack()
        self.search_entry = Entry(self.window)
        self.search_entry.pack()

        self.search_button = Button(self.window, text="Search", command=self.searchBook)
        self.search_button.pack()

    def updateBook(self):
        isbn = self.isbn_entry.get()
        bookId = Book.getBookIdByIsbn(isbn)
        title = self.title_entry.get()
        authors = self.author_entry.get()
        Book.updateBook(bookId, title, authors)
        messagebox.showinfo('Update', 'Book updated successfully!')

    def deleteBook(self):
        isbn = self.isbn_del_Entry.get()
        bookId = Book.getBookIdByIsbn(isbn)
        Book.deleteBook(bookId)
        messagebox.showinfo('Delete', 'Book deleted successfully!')
    def addBook(self):
        isbn = self.isbn_entry.get()
        title = self.title_entry.get()
        authors = self.author_entry.get()
        Book.addBook( title, authors,isbn)
        messagebox.showinfo('Add','Added Successfully!')

    def viewBorrowedBooks(self):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                  select book.isbn,book.title,borrow.borrowDate,borrow.userid from book,borrow
                  where borrow.bookId = book.Id
                  and borrow.status = :status
                  """, {'uId': self.Id, 'status': 'borrowed'})

        books = c.fetchall()
        print(books)

        if not books:
            messagebox.showinfo('Borrowed Books','No borrowed Books!')
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
                book = f"{i} -- {book[0]} -- {book[1]} -- {book[2]}"
                i+=1
                borrow_listbox.insert("end", book)

            borrow.mainloop()
            for book in books:
                print(f"{book[0]} - {book[1]} - {book[2]}")
            print('')

        conn.commit()
        conn.close()

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

    def getBorrowedBookforUser(self):
        pass

    def menu(self):
        while True:
            print("""
                  1. update books
                  2. view all borrowed books report
                  3. search for book
                  q. quit
                  """)
            choice = input("select your choice: ")
            f = {
                "1": self.updateBook,
                "2": self.viewBorrowedBooks,
                "3": self.searchBook,
                "q": 'q'}.get(choice, None)
            if f == 'q':
                break
            if f == None:
                print("Error, Try Again..")

            else:
                f()

    def foo(self):
        pass
    def run(self):
        self.window.mainloop()