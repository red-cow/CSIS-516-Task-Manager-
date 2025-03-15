# My other Python classes
from Style import UIStyle
from Driver import Database_Driver
from Visibility import Show

# Other Peoples Python Packages
from datetime import datetime
from PIL import Image, ImageTk # pillow
import tkinter as tk
from tkcalendar import Calendar


class TimeManagerTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Manager")
        self.root.geometry("1000x900")
        self.root.resizable(False, False)

        self.user = ["", "", "", ""]

        # --- Dictionary to store frames ---
        self.frames = {}

        # Create a container frame to hold all screens
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # --- Frame Creation ---
        self.frames["home"] = tk.Frame(self.container)
        self.frames["login"] = tk.Frame(self.container, bg="lightgray")
        self.frames["create_account"] = tk.Frame(self.container)
        self.frames["calendar"] = tk.Frame(self.container)

        # --- Place all frames in the same position ---
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Stack all frames

        # --- Home Screen ---
        self.lbl_welcome = tk.Label(self.frames["home"], text="Welcome to Time Manager")
        self.lbl_welcome.pack(pady=20)

        self.btn_create_task = tk.Button(self.frames["home"], text="Go to Calendar",
                                         command=lambda: self.show_frame("calendar"))
        self.btn_create_task.pack()

        self.btn_logout = tk.Button(self.frames["home"], text="Logout", command=lambda: self.show_frame("login"))
        self.btn_logout.pack()

        # --- Calendar Screen ---
        lbl_calendar = tk.Label(self.frames["calendar"], text="Calendar View")
        lbl_calendar.pack(pady=20)

        btn_back_calendar = tk.Button(self.frames["calendar"], text="Back", command=lambda: self.show_frame("home"))
        btn_back_calendar.pack()

        # --- Login Screen ---
        lbl_login = tk.Label(self.frames["login"], text="Login Screen")
        lbl_login.pack(pady=20)

        btn_login = tk.Button(self.frames["login"], text="Login", command=lambda: self.show_frame("home"))
        btn_login.pack()

        btn_create_account = tk.Button(self.frames["login"], text="Create Account",
                                       command=lambda: self.show_frame("create_account"))
        btn_create_account.pack()

        # --- Create Account Screen ---
        lbl_create_account = tk.Label(self.frames["create_account"], text="Create an Account")
        lbl_create_account.pack(pady=20)

        btn_back_to_login = tk.Button(self.frames["create_account"], text="Back to Login",
                                      command=lambda: self.show_frame("login"))
        btn_back_to_login.pack()

        # --- Show Login Screen Initially ---
        self.show_frame("login")

    def show_frame(self, frame_name):
        """Hide all frames and show only the selected one."""
        for frame in self.frames.values():
            frame.place_forget()  # Hide all frames
        self.frames[frame_name].place(relx=0, rely=0, relwidth=1, relheight=1)  # Show selected frame

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



    def show_create_task(self):
        self.home_frame.grid_forget()
        self.create_task_frame.grid(row=0, column=0, sticky="nsew")


        #Database Connection

    # event  handlers
    def login(self):
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()


        user_input = self.txt_email_ln.get("1.0", "end-1c").strip()
        self.cursor.execute("SELECT * FROM User WHERE Email = ?", (user_input,))
        try:
            result = self.cursor.fetchone()
            if result and result[3] == self.txt_password_ln.get():
                self.user = result
                Show.show_home(self)
            else:
                self.show_login_fail_message()  # Now always executed if login fails
        except Exception as e:
            print(f"Error: {e}")  # Helps debug if something is wrong

    def create_account(self):
        if hasattr(self, 'lbl_create_account_fail'):
            self.lbl_create_account_fail.destroy()
        name = self.txt_name.get("1.0", "end-1c")
        email = self.txt_email_ca.get("1.0", "end-1c")
        passowrd = self.txt_password_ca.get()

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
app = TimeManagerTest(root)
root.mainloop()
