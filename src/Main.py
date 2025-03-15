# My other Python classes
from Style import UIStyle
from Driver import Database_Driver
#from Visibility import Show

# Other Peoples Python Packages
from datetime import datetime
from PIL import Image, ImageTk # pillow 
import tkinter as tk
from tkcalendar import Calendar


class TimeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Manager")
        self.root.geometry("1000x900")
        self.root.resizable(False,False)

        self.user = ["","","",""]

        # --- Dictionary to store frames ---
        self.frames = {}

        # Create a container frame to hold all screens
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # --- Frame Creation ---
        self.frames["home"] = tk.Frame(self.container, bg=UIStyle.COLORS["bg"])
        self.frames["login"] = tk.Frame(self.container, bg=UIStyle.COLORS["bg"])
        self.frames["create_account"] = tk.Frame(self.container, bg=UIStyle.COLORS["bg"])
        self.frames["calendar"] = tk.Frame(self.container, bg=UIStyle.COLORS["bg"])
        self.frames["task_create"] = tk.Frame(self.container, bg=UIStyle.COLORS["bg"])

        # --- Place all frames in the same position ---
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Stack all frames

        # --- Home Screen ---

        self.lbl_welcome = tk.Label(self.frames["home"])
        self.lbl_welcome.grid(row=1, column=0, columnspan = 4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_welcome)

        self.btn_create_task = tk.Button(self.frames["home"])
        self.btn_create_task.grid(row=1, column=5, sticky="ew")
        UIStyle.apply_button_style(self.btn_create_task, "+",command=lambda: self.show_frame("login"))

        self.lbl_date = tk.Label(self.frames["home"]) #, font=("Arial", 20), fg="white", bg="black", padx=20, pady=10)
        self.lbl_date.grid(row =2, column=0, columnspan=4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_date)

        self.icon = Image.open("Clock.jpg").resize((100,100))
        self.icon = ImageTk.PhotoImage(self.icon)

        self.btn_calandar_view = tk.Button(self.frames["home"], image=self.icon, command=lambda: self.show_frame("calendar"))
        self.btn_calandar_view.grid(row=3, column=1)



        self.btn_list_view = tk.Button(self.frames["home"], text= "view")
        self.btn_list_view.grid(row= 3, column=3)



        self.app_icon = Image.open("FileIcon.png").resize((100,100))
        self.app_icon = ImageTk.PhotoImage(self.app_icon)
        self.root.iconphoto(True, self.app_icon)
        # --- Create Task Screen ---

        self.lbl_task_name = tk.Label(self.frames["task_create"])
        self.lbl_task_name.grid(row = 1, column=0)
        UIStyle.apply_label_style(self.lbl_task_name, text="Task")



        # --- Calendar Screen (Second Frame) ---

        lbl_calendar = tk.Label(self.frames["calendar"], text="Calendar View")
        lbl_calendar.grid(row =0, column=0, columnspan=4, sticky="ew")

        btn_back = tk.Button(self.frames["calendar"], text="Back", command=lambda: self.show_frame("home"))#.grid(row =1 , column=0, columnspan=4, sticky="ew")
        btn_back.grid(row=1, column=0, columnspan=4, sticky="ew")

        # --- Login Screen () ---

        self.lbl_login = tk.Label(self.frames["login"])
        self.lbl_login.grid(row =0, column=1, columnspan=3, sticky="ew")
        UIStyle.apply_label_style(self.lbl_login,"Please Enter your email password")

        self.lbl_email = tk.Label(self.frames["login"])
        self.lbl_email.grid(row=1, column=1,sticky="ew")
        UIStyle.apply_label_style(self.lbl_email, "Email:")

        self.txt_email_ln = tk.Text(self.frames["login"])#, height=1, width=30)
        self.txt_email_ln.grid(row=1, column=2)
        self.txt_email_ln.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_email_ln)

        self.lbl_password = tk.Label(self.frames["login"])
        self.lbl_password.grid(row=2, column=1, sticky="ew")
        UIStyle.apply_label_style(self.lbl_password,  text="Password:")

        self.txt_password_ln = tk.Entry(self.frames["login"])
        self.txt_password_ln.grid(row=2, column=2)
        self.txt_password_ln.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_password_ln)


        self.btn_submit = tk.Button(self.frames["login"], text="Submit", command=self.login)
        self.btn_submit.grid(row=3, column=1, columnspan=2)

        self.lbl_crate_account = tk.Label(self.frames["login"])
        self.lbl_crate_account.grid(row=5, column=1, columnspan=2)
        UIStyle.apply_label_style(self.lbl_crate_account, text="Don't have an account? Click here to create one.", font="body")

        self.btn_create_account = tk.Button(self.frames["login"], text="Create Account",command= lambda: self.show_frame("create_account"))
        self.btn_create_account.grid(row=6, column=1, columnspan=2)

        # -- create account screen ()--

        self.lbl_create_account = tk.Label(self.frames["create_account"])
        self.lbl_create_account.grid(row=0, column=0, columnspan=3, sticky="ew")
        UIStyle.apply_label_style(self.lbl_create_account, text="Please Enter in your information below")

        self.lbl_email = tk.Label(self.frames["create_account"], )
        self.lbl_email.grid(row=1, column=1)
        UIStyle.apply_label_style(self.lbl_email, text="Email:")

        self.txt_email_ca = tk.Text(self.frames["create_account"], height=1, width=30)
        self.txt_email_ca.grid(row=1, column=2)
        self.txt_email_ca.bind("<Tab>", self.focus_next_widget)

        self.lbl_name = tk.Label(self.frames["create_account"], text="Name:")
        self.lbl_name.grid(row=2, column=1)

        self.txt_name = tk.Text(self.frames["create_account"], height=1, width=30)
        self.txt_name.grid(row=2, column=2)
        self.txt_name.bind("<Tab>", self.focus_next_widget)

        self.lbl_password = tk.Label(self.frames["create_account"], text="Password:")
        self.lbl_password.grid(row=4, column=1)

        self.txt_password_ca = tk.Entry(self.frames["create_account"], width=30, show="*")
        self.txt_password_ca.grid(row=4, column=2)
        self.txt_password_ca.bind("<Tab>", self.focus_next_widget)

        self.date_dob_ca = Calendar(self.frames["create_account"], selectmode="day", date_pattern="yyyy-mm-dd")
        self.date_dob_ca.grid(row=5, column=1 , columnspan = 3,  pady=10)
        UIStyle.apply_calendar_style(self.date_dob_ca)

        self.btn_new_account = tk.Button(self.frames["create_account"])
        self.btn_new_account.grid(row=6, column=2)
        UIStyle.apply_button_style(self.btn_new_account, "Create Account", command=lambda: self.show_frame("home"))

        self.btn_back = tk.Button(self.frames["create_account"])
        self.btn_back.grid(row=0, column=3)
        UIStyle.apply_button_style(self.btn_back, text="Back To login", command=lambda: self.show_frame("login"), bg="danger")

        self.show_frame("login")
        self.update_time()
        Database_Driver.Driver(self)

    # background tasks

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%B %d, %Y %I:%M %p")
        self.lbl_date.config(text=current_time)
        self.lbl_date.after(1000, self.update_time)

        # visibility functions
    def show_frame(self, frame_name):
        """Hide all frames and show only the selected one."""
        for frame in self.frames.values():
            frame.place_forget()  # Hide all frames
        self.frames[frame_name].place(relx=0, rely=0, relwidth=1, relheight=1)  # Show selected frame



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
                self.show_frame("home")
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

        self.lbl_create_account_fail = tk.Label(self.frames["create_account"], text=f"You forgot to fill out fields:" , fg=UIStyle.COLORS["danger"], bg=UIStyle.COLORS["bg"])
        self.lbl_create_account_fail.grid(row=4, column=1, columnspan=3, sticky="ew")

        self.root.update()  # Force UI refresh
    def show_login_fail_message(self):
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()  # Prevents duplicate labels

        self.lbl_login_fail = tk.Label(self.frames["login"], text="Either password or username was incorrect", fg=UIStyle.COLORS["danger"], bg=UIStyle.COLORS["bg"])
        self.lbl_login_fail.grid(row=4, column=0, columnspan=3, sticky="ew")

        self.root.update()  # Force UI refresh

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"


root = tk.Tk()
app = TimeManager(root)
root.mainloop()
