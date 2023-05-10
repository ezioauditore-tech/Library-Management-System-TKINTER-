from tkinter import *
from tkinter import messagebox
from user import User
from member import Memebr
from librarian import Librarian

class BcuLibSystem:
    def __init__(self, master):
        self.master = master
        master.title("BCU Lib System")

        self.welcome_label = Label(master, text="Welcome to BCU Lib System")
        self.welcome_label.pack()

        self.login_button = Button(master, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = Button(master, text="Register", command=self.register)
        self.register_button.pack()

    def login(self):
        login_window = Toplevel(self.master)
        login_window.title("Login")

        uid_label = Label(login_window, text="User ID")
        uid_label.pack()

        self.uid_entry = Entry(login_window)
        self.uid_entry.pack()

        pswd_label = Label(login_window, text="Password")
        pswd_label.pack()

        self.pswd_entry = Entry(login_window, show="*")
        self.pswd_entry.pack()

        login_button = Button(login_window, text="Login", command=self.validate_login)
        login_button.pack()

    def validate_login(self):
        uid = self.uid_entry.get()
        pswd = self.pswd_entry.get()

        result = User.login(uid, pswd)

        if result['IsExist']:
            messagebox.showinfo("Login Successful", f"Welcome {result['Name']}")
            if result['Role'] == 'staff' or result['Role'] == 'student':
                m = Memebr(result['Id'])
                m.run()
            if result['Role'] == 'lib':
                m = Librarian(result['Id'])
                m.run()
        else:
            messagebox.showerror("Login Failed", "Invalid User ID or Password")

    def register(self):
        register_window = Toplevel(self.master)
        register_window.title("Register")

        u_name_label = Label(register_window, text="Username")
        u_name_label.pack()

        self.u_name_entry = Entry(register_window)
        self.u_name_entry.pack()

        uid_label = Label(register_window, text="User ID")
        uid_label.pack()

        self.uid_entry = Entry(register_window)
        self.uid_entry.pack()

        pswd_label = Label(register_window, text="Password")
        pswd_label.pack()

        self.pswd_entry = Entry(register_window, show="*")
        self.pswd_entry.pack()

        role_label = Label(register_window, text="User Role (staff or student)")
        role_label.pack()

        self.role_entry = Entry(register_window)
        self.role_entry.pack()

        register_button = Button(register_window, text="Register", command=self.validate_register)
        register_button.pack()

    def validate_register(self):
        u_name = self.u_name_entry.get()
        uid = self.uid_entry.get()
        pswd = self.pswd_entry.get()
        role = self.role_entry.get()

        User.register(u_name, uid, pswd, role)

        messagebox.showinfo("Registration Successful", "Your account has been created. Please login.")

        self.login()

root = Tk()
app = BcuLibSystem(root)
root.mainloop()
