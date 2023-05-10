class Book:
    
    def addBook():
        pass
    
    def deleteBook():
        pass
    
    def updateBook(bookId, title, authors):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                      update book set
                      title = :titl, authors = :auth
                      where id = :bid
                      """ , {'titl' : title, 'bid':bookId, 'auth' : authors})
        print("Book is modified successfully")
        conn.commit()
        conn.close()
    
    def checkAvailbality(bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()


        c.execute("""
                  select available from Book
                  where id = :bid          
                  """,{'bid':bookId})

        ava = c.fetchone()[0]
        conn.close()
        return ava
    
    def updateAvailibility(number, bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                      update book set
                      available = :nava
                      where id = :bid
                      """ , {'nava' : number, 'bid':bookId})
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def getBookIdByIsbn(isbn):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                  select id from Book
                  where isbn = :is          
                  """,{'is':isbn})
        result = c.fetchone()
        
        conn.commit()
        conn.close()
        return result[0]