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

        self.user = ""


        # --- Home Screen ---
        self.home_frame = tk.Frame(root)
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

        btn_back = tk.Button(self.calendar_frame, text="Back", command=self.show_home)#.grid(row =1 , column=0, columnspan=4, sticky="ew")
        btn_back.grid(row =1 , column=0, columnspan=4, sticky="ew")

        # --- Login Screen () ---

        self.login_frame = tk.Frame(root)

        self.lbl_login = tk.Label(self.login_frame)
        self.lbl_login.grid(row =0, column=1, columnspan=3, sticky="ew")
        UIStyle.apply_label_style(self.lbl_login,"Please Enter your email password")

        self.lbl_email = tk.Label(self.login_frame)
        self.lbl_email.grid(row=1, column=1,sticky="ew")
        UIStyle.apply_label_style(self.lbl_email, "Email:")

        self.txt_email_ln = tk.Text(self.login_frame, height=1, width=30)
        self.txt_email_ln.grid(row=1, column=2)
        self.txt_email_ln.bind("<Tab>", self.focus_next_widget)
        #UIStyle.apply_entry_style(self.txt_email_ln, "")

        self.lbl_password = tk.Label(self.login_frame, text="Password:")
        self.lbl_password.grid(row=2, column=1)

        self.txt_password_ln = tk.Entry(self.login_frame, width=30, show="*")
        self.txt_password_ln.grid(row=2, column=2)
        self.txt_password_ln.bind("<Tab>", self.focus_next_widget)
       # UIStyle.apply_entry_style(self.txt_email_ln)


        self.btn_submit = tk.Button(self.login_frame, text="Submit", command=self.login)
        self.btn_submit.grid(row=3, column=2)

        self.lbl_crate_account = tk.Label(self.login_frame, text="Don't have an account? Click here to cerate one.")
        self.lbl_crate_account.grid(row=5, column=2)

        self.btn_create_account = tk.Button(self.login_frame, text="Create Account",command=self.show_create_account)
        self.btn_create_account.grid(row=6, column=2)

        # -- create account screen ()--

        self.create_account_frame = tk.Frame(root)

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

        self.btn_back= tk.Button(self.create_account_frame, text="Back To login", command=self.show_login)
        self.btn_back.grid(row=5, column=2)


        self.show_login()
        self.update_time()
        self.Driver()

    # background tasks

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%B %d, %Y %I:%M %p")
        self.lbl_date.config(text=current_time)
        self.lbl_date.after(1000, self.update_time)

        # visibility functions

    def show_home(self):
        self.calendar_frame.grid_forget()
        self.login_frame.grid_forget()
        self.lbl_welcome.config(text=f"Hello, {self.user[1]}")
        self.home_frame.grid(row=0, column=0, sticky="nsew")

    def show_calendar(self):
        self.home_frame.grid_forget()
        self.calendar_frame.grid(row=0, column=0, sticky="nsew")

    def show_login(self):
        self.create_account_frame.grid_forget()
        self.home_frame.grid_forget()
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()

        self.login_frame.grid(row=0, column=0, sticky="nsew")

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
                self.show_home()
            else:
                self.show_login_fail_message()  # Now always executed if login fails
        except Exception as e:
            print(f"Error: {e}")  # Helps debug if something is wrong

    def show_login_fail_message(self):
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()  # Prevents duplicate labels

        self.lbl_login_fail = tk.Label(self.login_frame, text="Either password or username was incorrect", fg="red")
        self.lbl_login_fail.grid(row=4, column=0, columnspan=3, sticky="ew")

        self.root.update()  # Force UI refresh

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

class UIStyle:
    COLORS = {
        "bg": "#2C3E50",
        "fg": "#ECF0F1",
        "primary": "#27AE60",
        "secondary": "#2980B9",
        "danger": "#E74C3C",
        "input_bg": "#FFFFFF",
        "input_fg": "#333333",
        "border": "#BDC3C7"
    }

    FONTS = {
        "heading": ("Helvetica", 20, "bold"),
        "subheading": ("Helvetica", 16, "bold"),
        "body": ("Helvetica", 12),
        "button": ("Helvetica", 12, "bold"),
        "input": ("Helvetica", 12)
    }

    @staticmethod
    def apply_label_style(widget, text=""):
        widget.config(
            text=text,
            font=UIStyle.FONTS["heading"],
            bg=UIStyle.COLORS["bg"],
            fg=UIStyle.COLORS["fg"],
            padx=20,
            pady=10
        )

    @staticmethod
    def apply_button_style(widget, text="", command=None):
        widget.config(
            text=text,
            font=UIStyle.FONTS["button"],
            bg=UIStyle.COLORS["primary"],
            fg="white",
            activebackground="#218C53",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            command=command
        )

    @staticmethod
    def apply_entry_style(widget, placeholder=""):
        widget.config(
            font=UIStyle.FONTS["input"],
            bg=UIStyle.COLORS["input_bg"],
            fg=UIStyle.COLORS["input_fg"],
            insertbackground=UIStyle.COLORS["input_fg"],
            highlightbackground=UIStyle.COLORS["border"],
            highlightcolor=UIStyle.COLORS["primary"],
            borderwidth=2,
            relief="groove"
        )
        widget.insert(0, placeholder)

root = tk.Tk()
app = TimeManager(root)
root.mainloop()
