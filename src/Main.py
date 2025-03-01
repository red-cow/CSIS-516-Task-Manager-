# My other Python classes
from Style import UIStyle
from Driver import Database_Driver
from Visibility import Show

# Other Poeples Python Packages
from datetime import datetime
from PIL import Image, ImageTk # pillow
import tkinter as tk
import sqlite3

class TimeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Manager")
        self.root.geometry("1000x900")
        self.root.resizable(False,False)

        self.user = ["","","",""]

        # --- frame creation ---
        self.home_frame = tk.Frame(root)

        self.login_frame = tk.Frame(root, bg=UIStyle.COLORS["bg"], height=1000, width=1000)
        self.create_account_frame = tk.Frame(root)

        # --- Home Screen ---

        self.home_frame.grid(row=0, column=0, sticky="nsew")

        self.lbl_welcome = tk.Label(self.home_frame)
        self.lbl_welcome.grid(row=1, column=0, columnspan = 4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_welcome)

        self.btn_create_task = tk.Button(self.home_frame)
        self.btn_create_task.grid(row=1, column=5, sticky="ew")
        UIStyle.apply_button_style(self.btn_create_task, "+",command=self.show_create_task)

        self.lbl_date = tk.Label(self.home_frame) #, font=("Arial", 20), fg="white", bg="black", padx=20, pady=10)
        self.lbl_date.grid(row =2, column=0, columnspan=4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_date)

        self.icon = Image.open("Clock.jpg").resize((100,100))
        self.icon = ImageTk.PhotoImage(self.icon)

        self.btn_calandar_view = tk.Button(self.home_frame, image=self.icon, command=self.show_calendar)
        self.btn_calandar_view.grid(row=3, column=1)



        self.btn_list_view = tk.Button(self.home_frame, text= "view")
        self.btn_list_view.grid(row= 3, column=3)



        self.app_icon = Image.open("FileIcon.png").resize((100,100))
        self.app_icon = ImageTk.PhotoImage(self.app_icon)
        self.root.iconphoto(True, self.app_icon)
        # --- Create Task Screen ---

        self.create_task_frame = tk.Frame(root)

        # --- Calendar Screen (Second Frame) ---
        self.calendar_frame = tk.Frame(root)

        lbl_calendar = tk.Label(self.calendar_frame, text="Calendar View", font=("Arial", 14)).grid(row =0, column=0, columnspan=4, sticky="ew")

        btn_back = tk.Button(self.calendar_frame, text="Back", command=Show.show_home(self))#.grid(row =1 , column=0, columnspan=4, sticky="ew")
        btn_back.grid(row=1, column=0, columnspan=4, sticky="ew")

        # --- Login Screen () ---

        self.lbl_login = tk.Label(self.login_frame)
        self.lbl_login.grid(row =0, column=1, columnspan=3, sticky="ew")
        UIStyle.apply_label_style(self.lbl_login,"Please Enter your email password")

        self.lbl_email = tk.Label(self.login_frame)
        self.lbl_email.grid(row=1, column=1,sticky="ew")
        UIStyle.apply_label_style(self.lbl_email, "Email:")

        self.txt_email_ln = tk.Text(self.login_frame)#, height=1, width=30)
        self.txt_email_ln.grid(row=1, column=2)
        self.txt_email_ln.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_email_ln)

        self.lbl_password = tk.Label(self.login_frame)
        self.lbl_password.grid(row=2, column=1, sticky="ew")
        UIStyle.apply_label_style(self.lbl_password,  text="Password:")

        self.txt_password_ln = tk.Entry(self.login_frame)
        self.txt_password_ln.grid(row=2, column=2)
        self.txt_password_ln.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_password_ln)


        self.btn_submit = tk.Button(self.login_frame, text="Submit", command=self.login)
        self.btn_submit.grid(row=3, column=2)

        self.lbl_crate_account = tk.Label(self.login_frame, text="Don't have an account? Click here to cerate one.")
        self.lbl_crate_account.grid(row=5, column=2)

        self.btn_create_account = tk.Button(self.login_frame, text="Create Account",command=self.show_create_account)
        self.btn_create_account.grid(row=6, column=2)

        # -- create account screen ()--

        self.lbl_create_account = tk.Label(self.create_account_frame, text="Please Enter in your information below", font=("Arial", 20),  fg="white", bg="black", padx=20, pady=10)
        self.lbl_create_account.grid(row=0, column=1, columnspan=3, sticky="ew")

        self.lbl_email = tk.Label(self.create_account_frame, text="Email:")
        self.lbl_email.grid(row=1, column=1)

        self.txt_email_ca = tk.Text(self.create_account_frame, height=1, width=30)
        self.txt_email_ca.grid(row=1, column=2)
        self.txt_email_ca.bind("<Tab>", self.focus_next_widget)

        self.lbl_name = tk.Label(self.create_account_frame, text="Name:")
        self.lbl_name.grid(row=2, column=1)

        self.txt_name = tk.Text(self.create_account_frame, height=1, width=30)
        self.txt_name.grid(row=2, column=2)
        self.txt_name.bind("<Tab>", self.focus_next_widget)

        self.lbl_password = tk.Label(self.create_account_frame, text="Password:")
        self.lbl_password.grid(row=4, column=1)

        self.txt_password_ca = tk.Entry(self.create_account_frame, width=30, show="*")
        self.txt_password_ca.grid(row=4, column=2)
        self.txt_password_ca.bind("<Tab>", self.focus_next_widget)

        self.btn_new_account = tk.Button(self.create_account_frame)
        self.btn_new_account.grid(row=5, column=2)
        UIStyle.apply_button_style(self.btn_new_account, "Create Account", )

        self.btn_back = tk.Button(self.create_account_frame, text="Back To login", command=Show.show_login(self))
        self.btn_back.grid(row=6, column=2)


        Show.show_login(self)
        self.update_time()
        self.Driver()

    # background tasks

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%B %d, %Y %I:%M %p")
        self.lbl_date.config(text=current_time)
        self.lbl_date.after(1000, self.update_time)

        # visibility functions



    def show_calendar(self):
        self.home_frame.grid_forget()
        self.calendar_frame.grid(row=0, column=0, sticky="nsew")



    def show_create_account(self):
        self.login_frame.grid_forget()
        self.create_account_frame.grid(row=0, column=0, sticky="nsew")

    def show_create_task(self):
        self.home_frame.grid_forget()
        self.create_task_frame.grid(row=0, column=0, sticky="nsew")


        #Database Connection
    def Driver(self):
        self.conn = sqlite3.connect("TaskManager.db")
        self.cursor = self.conn.cursor()

    # event  handlers
    def login(self):
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()


        user_input = self.txt_email_ln.get("1.0", "end-1c").strip()
        self.cursor.execute("SELECT * FROM User WHERE Email = ?", (user_input,))
        try:
            result = self.cursor.fetchone()
            if result and result[3] == self.txt_password_ln.get().strip():
                self.user = result
                Show.show_home(self)
            else:
                self.show_login_fail_message()  # Now always executed if login fails
        except Exception as e:
            print(f"Error: {e}")  # Helps debug if something is wrong

    def create_account(self):
        if hasattr(self, 'lbl_create_account_fail'):
            self.lbl_create_account_fail.destroy()

    def show_create_account_fail_message(self):
        if hasattr(self, 'lbl_create_account_fail'):
            self.lbl_create_account_fail.destroy()

        self.lbl_create_account_fail = tk.Label(self.login_frame, text=f"You forgot to fill out fields:" , fg="red")
        self.lbl_create_account_fail.grid(row=4, column=0, columnspan=3, sticky="ew")

        self.root.update()  # Force UI refresh
    def show_login_fail_message(self):
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()  # Prevents duplicate labels

        self.lbl_login_fail = tk.Label(self.login_frame, text="Either password or username was incorrect", fg="red")
        self.lbl_login_fail.grid(row=4, column=0, columnspan=3, sticky="ew")

        self.root.update()  # Force UI refresh

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"


root = tk.Tk()
app = TimeManager(root)
root.mainloop()
