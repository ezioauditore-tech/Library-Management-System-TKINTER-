from book import Book
import datetime
import tkinter as tk
from tkinter import messagebox


class LibData:

    @staticmethod
    def borrowBook(userId, bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        ava = Book.checkAvailbality(bookId)
        if ava > 0:
            today = datetime.date.today()
            today = today.strftime("%d/%m/%Y")
            c.execute("""
                      insert into borrow(userId,bookId,borrowDate,status)
                      values(:uid,:bid,:bdate,:status)              
                      """, {'uid': userId, 'bid': bookId, 'bdate': today, 'status': 'borrowed'})
            conn.commit()
            conn.close()
            Book.updateAvailibility(ava - 1, bookId)
            messagebox.showinfo('Borrow Book', 'Book is borrowed by you')
        else:
            messagebox.showinfo('Borrow Book', 'The book is not available')

    @staticmethod
    def reserveBook(userId, bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        today = datetime.date.today()
        today = today.strftime("%d/%m/%Y")
        c.execute("""
                    insert into reserve(userId,bookId,reserveDate,status)
                    values(:uid,:bid,:bdate,:status)              
                    """, {'uid': userId, 'bid': bookId, 'bdate': today, 'status': 'reserved'})
        conn.commit()
        conn.close()
        messagebox.showinfo('Reserve Book', 'Book has been reserved successfully')

    @staticmethod
    def returnBook(bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        ava = Book.checkAvailbality(bookId)
        today = datetime.date.today()
        today = today.strftime("%d/%m/%Y")
        c.execute(
            "UPDATE borrow SET returnDate = :return_date, status = 'returned' WHERE bookId = :bookId",
            {"return_date": today, "bookId": bookId})
        conn.commit()
        conn.close()
        Book.updateAvailibility(ava - 1, bookId)
        messagebox.showinfo('Return Book', 'Book returned successfully')

    @staticmethod
    def searchBook(data):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        data = '%' + data + '%'
        c.execute(""" 
                  select title, authors, isbn from book
                  where title like :d
                  or authors like :d
                  or isbn like :d                  
                  """, {'d': data})
        result = c.fetchall()
        book_list = "ISBN - Title - Authors\n"
        i = 1
        for book in result:
            book_list += f"{i} - {book[2]} - {book[0]} - {book[1]}\n"
            i += 1
        conn.commit()
        conn.close()
        return result

    @staticmethod
    def calculateFine(userId, bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                  select borrowDate, returnDate from borrow
                  where userId = :uid
                  and bookId = :bid
                  """, {'uid': userId, 'bid': bookId})
        result = c.fetchone()
        borrowDate = result[0]
        returnDate = result[1]
        bDate = datetime.datetime.strptime(borrowDate, "%d/%m/%Y")
        rDate = datetime.datetime.strptime(returnDate, "%d/%m/%Y")
        delta = rDate - bDate
        delta = delta.days
        if delta <= 7:
            messagebox.showinfo('Fine Calculation', "You don't owe any fine")
        else:
            fineDays = delta - 7
            messagebox.showinfo(
                'Fine Calculation',
                f"You returned the book after {delta} days.\n"
                f"The fine for everyday delay more than 7 days is 2 pound.\n"
                f"You have to pay {fineDays*2} pounds."
            )
        conn.commit()
        conn.close()

