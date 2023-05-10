class User:

    def __init__(self, Id):
        self.Id = Id

    @staticmethod
    def login(username, password):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                  select Id,Name,Role from user
                  where UserName = :uName
                  and Password = :pass
                  """, {'uName': username, 'pass': password})
        result = c.fetchone()

        if not result:
            return {'IsExist': False}
        else:
            return {'IsExist': True, 'Id': result[0], 'Name': result[1],
                    'Role': result[2]}
        conn.commit()
        conn.close()

    def register(u_name, uid, password, user_type):
        try:
            import sqlite3
            connection = sqlite3.connect("mydb.db")
            cur = connection.cursor()
            cur.execute("INSERT INTO User(name,userName,password,role) VALUES(?,?,?,?)",
                        (u_name, uid, password, user_type))
            connection.commit()
            connection.close()
            print('Success, Account created successfully')

        except Exception as e:
            print(
                'Error', 'Something went wrong, try again')
            print(e)
