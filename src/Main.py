# My other Python classes
from src.Style import UIStyle
from src.Driver import Database_Driver
from src.CalendarView import TaskCalendarApp
from src.CalendarPicker import PickDate
from src.ListView import TaskGallery
from src.AIComponents import ChatGPT

# Other Peoples Python Packages
import os
import sys
from datetime import datetime
from PIL import Image, ImageTk # pillow 
import tkinter as tk
from tkinter import ttk # gets you more tkinter controls
from tkcalendar import Calendar
from tkinter import messagebox
import threading


class TimeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Manager")
        self.root.geometry("1000x900")
        self.root.resizable(False,False)
        self.db = Database_Driver()
        self.ai = ChatGPT()

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
        self.frames["create_task"] = tk.Frame(self.container, bg=UIStyle.COLORS["bg"])
        self.frames["list_view"] = tk.Frame(self.container, bg=UIStyle.COLORS["bg"])


        # --- Place all frames in the same position ---
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Stack all frames

        # --- Home Screen ---

        self.frames["home"].grid_columnconfigure(0, weight=1)
        self.frames["home"].grid_columnconfigure(6, weight=1)

        self.lbl_welcome = tk.Label(self.frames["home"])
        self.lbl_welcome.grid(row=1, column=1, columnspan=4, sticky="ew")

        self.lbl_date = tk.Label(self.frames["home"]) #, font=("Arial", 20), fg="white", bg="black", padx=20, pady=10)
        self.lbl_date.grid(row =2, column=1, columnspan=4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_date)

        self.lbl_whats_recommend = tk.Label(self.frames["home"])
        self.lbl_whats_recommend.grid(row=5, column=1, columnspan=4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_whats_recommend, font="subheading", text="What to Do Next (AI Assisted)")

        self.lbl_ai_recomendation = tk.Label(self.frames["home"])
        self.lbl_ai_recomendation.grid(row=6,column=1, columnspan=4,sticky="ew")
        UIStyle.apply_label_style(self.lbl_ai_recomendation, text="AI generating response....", font="body",max_width=500)

        self.btn_ai_response_refresh = tk.Button(self.frames["home"])
        self.btn_ai_response_refresh.grid(row=6,column=5,stick="ew")
        UIStyle.apply_button_style(self.btn_ai_response_refresh, text="🔄", command=lambda: self.users_recommendation(self.db.GetTaskList(self.user[0])), width =2)

        self.btn_calandar_view = tk.Button(self.frames["home"], command=lambda: self.show_frame("calendar"))
        self.btn_calandar_view.grid(row=4, column=2, padx=10, pady=5)  # Add padding to space out buttons
        UIStyle.apply_button_style(self.btn_calandar_view, text="📅 Calendar View",width=12)
        self.btn_list_view = tk.Button(self.frames["home"])
        self.btn_list_view.grid(row=4, column=4, padx=10, pady=5)  # Add padding for spacing
        UIStyle.apply_button_style(self.btn_list_view, text="📜 List View", command=self.launch_list_view, width=12)

        self.btn_create_task = tk.Button(self.frames["home"])
        self.btn_create_task.grid(row=4, column=3, padx=10, pady=5, sticky="ew")  # Add padding and make it expand
        UIStyle.apply_button_style(self.btn_create_task, "➕ Add Task", command=lambda: self.show_frame("create_task"), width=12)

        self.btn_logout = tk.Button(self.frames["home"])
        self.btn_logout.grid(row=7, column=3, padx=10, pady=10)  # Add extra padding for the logout button
        UIStyle.apply_button_style(self.btn_logout, text="🚶‍♂️ logout", command=self.logout, bg="danger", width=12)

        if getattr(sys, 'frozen', False):
            # If running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_path = os.path.dirname(__file__)

        icon_path = os.path.join(base_path, "FileIcon.png")
        self.app_icon = Image.open(icon_path).resize((100, 100))
        self.app_icon = ImageTk.PhotoImage(self.app_icon)
        self.root.iconphoto(True, self.app_icon)
        # --- Create Task Screen ---

        self.frames["create_task"].grid_columnconfigure(0, weight=1)
        self.frames["create_task"].grid_columnconfigure(6, weight=1)

        self.lbl_task_name = tk.Label(self.frames["create_task"])
        self.lbl_task_name.grid(row=0, column=1, columnspan=5, pady=(10, 5))
        UIStyle.apply_label_style(self.lbl_task_name, text="Create a Task")

        # Labels for Title, Due Date, and Priority
        self.lbl_task_title = tk.Label(self.frames["create_task"])
        self.lbl_task_title.grid(row=1, column=1, sticky="w", padx=(10, 5), pady=(5, 2))
        UIStyle.apply_label_style(self.lbl_task_title, text="Title", font="subheading")

        self.lbl_due_date = tk.Label(self.frames["create_task"])
        self.lbl_due_date.grid(row=1, column=3, sticky="w", padx=(10, 5), pady=(5, 2))
        UIStyle.apply_label_style(self.lbl_due_date, text="Due Date", font="subheading")

        self.lbl_priority = tk.Label(self.frames["create_task"])
        self.lbl_priority.grid(row=1, column=5, sticky="w", padx=(10, 5), pady=(5, 2))
        UIStyle.apply_label_style(self.lbl_priority, text="Priority", font="subheading")

        # Title Textbox
        self.txt_task_title = tk.Text(self.frames["create_task"], height=1, width=30)
        self.txt_task_title.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.txt_task_title.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_task_title)

        # Due Date Selection Button
        self.btn_calendar_pull_up = tk.Button(self.frames["create_task"])
        self.btn_calendar_pull_up.grid(row=2, column=3, padx=10, pady=5)
        UIStyle.apply_button_style(self.btn_calendar_pull_up, text="Select Due Date",
                                   command=lambda: PickDate.open_date_picker(self))

        # Label to Display Selected Due Date
        self.date_label_task_created = tk.Label(self.frames["create_task"], text="No date selected")
        self.date_label_task_created.grid(row=2, column=4, padx=10, pady=5)
        UIStyle.apply_label_style(self.date_label_task_created, font="body")

        # Priority Dropdown Menu
        self.priority_var = tk.StringVar()
        self.priority_dropdown = ttk.Combobox(
            self.frames["create_task"],
            textvariable=self.priority_var,
            values=["Low", "Medium", "High", "Critical"],
            state="readonly",
            width=12
        )
        self.priority_dropdown.grid(row=2, column=5, padx=10, pady=5)
        self.priority_dropdown.current(1)

        self.lbl_description = tk.Label(self.frames["create_task"])
        self.lbl_description.grid(row=3, column=1, columnspan=5, padx=10, pady=5, stick="ew")
        UIStyle.apply_label_style(self.lbl_description, text="Description", font="subheading")

        self.txt_task_description = tk.Text(self.frames["create_task"])
        self.txt_task_description.grid(row=4, column=1, columnspan=5, padx=10, pady=5, sticky="ew")
        UIStyle.apply_entry_style(self.txt_task_description, height=20, width=80)

        # Create Task Button
        self.btn_create_new_task = tk.Button(self.frames["create_task"])
        self.btn_create_new_task.grid(row=5, column=2, columnspan=4, padx=10, pady=10)
        UIStyle.apply_button_style(self.btn_create_new_task, text="Create", command=self.create_task)

        self.btn_to_home = tk.Button(self.frames["create_task"])
        self.btn_to_home.grid(row=5, column=1)
        UIStyle.apply_button_style(self.btn_to_home, text="🔙 Back", bg="danger", command=lambda: self.show_frame("home"))

        # --- Login Screen () ---
        self.frames["login"].grid_columnconfigure(0, weight=1)
        self.frames["login"].grid_columnconfigure(1, weight=0)
        self.frames["login"].grid_columnconfigure(2, weight=0)
        self.frames["login"].grid_columnconfigure(3, weight=1)

        # Title
        self.lbl_login = tk.Label(self.frames["login"])
        self.lbl_login.grid(row=0, column=1, columnspan=2, pady=(20, 10), sticky ='nsew')
        UIStyle.apply_label_style(self.lbl_login, "Please enter your email and password")

        # Email
        self.lbl_email = tk.Label(self.frames["login"])
        self.lbl_email.grid(row=1, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_email, "Email:")

        self.txt_email_ln = tk.Text(self.frames["login"], height=1, width=50)
        self.txt_email_ln.grid(row=1, column=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_email_ln.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_email_ln)

        # Password
        self.lbl_password = tk.Label(self.frames["login"])
        self.lbl_password.grid(row=2, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_password, text="Password:")

        self.txt_password_ln = tk.Entry(self.frames["login"], show="*", width=50)
        self.txt_password_ln.grid(row=2, column=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_password_ln.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_password_ln)

        # Submit Button
        self.btn_submit = tk.Button(self.frames["login"])
        self.btn_submit.grid(row=3, column=1, columnspan=2, pady=10)
        UIStyle.apply_button_style(self.btn_submit, text="Submit", width=10, command=self.login)

        # Create Account Prompt
        self.lbl_crate_account = tk.Label(self.frames["login"])
        self.lbl_crate_account.grid(row=4, column=1, columnspan=2, pady=(20, 5))
        UIStyle.apply_label_style(self.lbl_crate_account, text="Don't have an account? Click below to create one.",
                                  font="body")

        # Create Account Button
        self.btn_create_account = tk.Button(self.frames["login"])
        self.btn_create_account.grid(row=6, column=1, columnspan=2, pady=5)
        UIStyle.apply_button_style(self.btn_create_account, text="Create Account", width=14,
                                   command=lambda: self.show_frame("create_account"))

        # -- create account screen ()--

        # Configure column weights for horizontal centering
        self.frames["create_account"].grid_columnconfigure(0, weight=1)  # Left spacer
        self.frames["create_account"].grid_columnconfigure(1, weight=0)  # Labels
        self.frames["create_account"].grid_columnconfigure(2, weight=0)  # Inputs
        self.frames["create_account"].grid_columnconfigure(3, weight=0)
        self.frames["create_account"].grid_columnconfigure(4, weight=1)  # Right spacer

        # Title
        self.lbl_create_account = tk.Label(self.frames["create_account"])
        self.lbl_create_account.grid(row=0, column=1, columnspan=3, pady=(20, 10), sticky="nsew")
        UIStyle.apply_label_style(self.lbl_create_account, text="Please Enter your information below")

        # Email
        self.lbl_email = tk.Label(self.frames["create_account"])
        self.lbl_email.grid(row=1, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_email, text="Email:")

        self.txt_email_ca = tk.Text(self.frames["create_account"], height=1, width=40)
        self.txt_email_ca.grid(row=1, column=2, columnspan=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_email_ca.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_email_ca)

        # Name
        self.lbl_name = tk.Label(self.frames["create_account"])
        self.lbl_name.grid(row=2, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_name, text="Name:")

        self.txt_name = tk.Text(self.frames["create_account"], height=1, width=40)
        self.txt_name.grid(row=2, column=2, columnspan=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_name.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_name)

        # Password
        self.lbl_password = tk.Label(self.frames["create_account"])
        self.lbl_password.grid(row=3, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_password, text="Password:")

        self.txt_password_ca = tk.Entry(self.frames["create_account"], show="*", width=40)
        self.txt_password_ca.grid(row=3, column=2, columnspan=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_password_ca.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_password_ca)

        # Date of Birth
        self.lbl_dob = tk.Label(self.frames["create_account"])
        self.lbl_dob.grid(row=4, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_dob, text="Birthday:")

        self.date_dob_ca = Calendar(self.frames["create_account"], selectmode="day", date_pattern="yyyy-mm-dd",
                                    maxdate=datetime.today().date())
        self.date_dob_ca.grid(row=4, column=2, sticky="w", pady=10)
        UIStyle.apply_calendar_style(self.date_dob_ca)

        # Buttons
        self.btn_new_account = tk.Button(self.frames["create_account"])
        self.btn_new_account.grid(row=5, column=2, pady=(10, 5))
        UIStyle.apply_button_style(self.btn_new_account, "Create Account", command=self.create_account, bg='primary')

        self.btn_back = tk.Button(self.frames["create_account"])
        self.btn_back.grid(row=5, column=4, pady=(10, 5), sticky='w')
        UIStyle.apply_button_style(self.btn_back, text="Back To Login", command=self.logout, bg="danger")


        self.lbl_password_req = tk.Label(self.frames["create_account"])
        self.lbl_password_req.grid(row=6, column=2, pady=(10, 5))
        UIStyle.apply_label_style(self.lbl_password_req, text="*Passwords must be at least 8 characters long*", font="body")

        # --- Calendar Frame (integrating TaskCalendarApp class) ---
        self.calendar_frame = TaskCalendarApp(self.frames["calendar"], self)  # Embed the TaskCalendarApp here

        # --- List View Frame (integrating TaskGallery class) ---
        self.list_view_frame = TaskGallery(self.frames["list_view"], self)  # Embed the TaskGallery here


        #self.show_frame("home")
        self.show_frame("login")
        self.update_time()

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
        if frame_name == "list_view":
                self.list_view_frame.main(self.frames["list_view"], self)
        if frame_name == "calendar":
                self.calendar_frame.main(self.frames["calendar"], self)


    # event  handlers
    def login(self):
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()

        user_email = self.txt_email_ln.get("1.0", "end-1c").strip()
        try:
            result = self.db.GetUser(user_email)
            if result and result[3] == self.txt_password_ln.get():
                self.user = result
                print(self.user)
                UIStyle.apply_label_style(self.lbl_welcome, text=f"Welcome {self.user[1]}")
                temp = self.db.GetTaskList(self.user[0])
                threading.Thread(target=lambda: self.users_recommendation(temp), daemon=True).start()
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
        password = self.txt_password_ca.get()
        dob = self.date_dob_ca.get_date()
        if not name.strip() or not email.strip() or not password.strip() or not dob.strip() or len(password) < 8:
            print("Error: All fields must be filled!")
            password_under_8_char = (len(password) < 8)
            empty_fields = [field_name for field_name, value in {
                "Name": name.strip(),
                "Email": email.strip(),
                "Password": password.strip(),
                "Date of Birth": dob.strip()
            }.items() if not value]
            self.show_create_account_fail_message(password_under_8_char, empty_fields)
        else:
            try:
                result = self.db.CreateUser(email, name, dob, password)
                print(result)
                self.user = result
                self.txt_name.delete("1.0", "end")
                self.txt_email_ca.delete("1.0", "end")
                self.txt_password_ca.delete(0, "end")

                UIStyle.apply_label_style(self.lbl_welcome, text=f"Welcome {self.user[1]}")
                temp = self.db.GetTaskList(self.user[0])
                threading.Thread(target=lambda: self.users_recommendation(temp), daemon=True).start()

                self.show_frame("home")
            except Exception as e:
                print(e)

    def logout(self):
        self.user = ["","","",""]
        self.txt_email_ln.delete("1.0", "end")
        self.txt_password_ln.delete(0, "end")
        self.txt_email_ca.delete("1.0", "end")
        self.txt_name.delete("1.0", "end")
        self.txt_password_ca.delete(0, "end")
        UIStyle.apply_label_style(self.lbl_ai_recomendation, text="AI generating response....", font="body",
                                  max_width=500) #removes the last users AI response to avoid confusion while the new one loads
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()

        if hasattr(self, 'lbl_create_account_fail'):
            self.lbl_create_account_fail.destroy()

        self.show_frame("login")

    def create_task(self):
        try:
            date_text = self.date_label_task_created.cget("text")
            date_value = date_text.split(": ")[1]
            return_value = self.db.CreateTask(self.priority_var.get(), self.txt_task_description.get("1.0", "end-1c"), self.txt_task_title.get("1.0", "end-1c"), date_value,self.user[0])
            if not(return_value):
                tk.messagebox.showerror("Task not created", "Some fields were left blank")
            else:
                tk.messagebox.showinfo("Success", "Task Created Successfully")
                self.txt_task_title.delete("1.0","end")
                self.txt_task_description.delete("1.0", "end")
                self.priority_dropdown.current(1)
                self.show_frame("home")
        except Exception as e:
            tk.messagebox.showerror("Task not created", "Some fields were left blank")


    def show_create_account_fail_message(self, password_not_over_8, empty_fields):
        if hasattr(self, 'lbl_create_account_fail'):
            self.lbl_create_account_fail.destroy()
        text = ""
        print(password_not_over_8)
        if len(empty_fields) != 0:
            text += f"You forgot to fill out field(s): {', '.join(empty_fields)}. "
        if not password_not_over_8:
            self.lbl_password_req.destroy()
        else:
            self.lbl_password_req = tk.Label(self.frames["create_account"])
            self.lbl_password_req.grid(row=6, column=2, pady=(10, 5))
            UIStyle.apply_label_style(self.lbl_password_req, text="*Passwords must be at least 8 characters long*", font="body")

        self.lbl_create_account_fail = tk.Label(self.frames["create_account"], text= text, fg=UIStyle.COLORS["danger"], bg=UIStyle.COLORS["bg"])
        self.lbl_create_account_fail.grid(row=8, column=2, pady=(10, 5))

        self.root.update()  # Force UI refresh
    def show_login_fail_message(self):
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()  # Prevents duplicate labels

        self.lbl_login_fail = tk.Label(self.frames["login"], text="Either password or username was incorrect", fg=UIStyle.COLORS["danger"], bg=UIStyle.COLORS["bg"])
        self.lbl_login_fail.grid(row=5, column=1, columnspan=2, pady=(20, 5))

        self.root.update()  # Force UI refresh

    def users_recommendation(self, task_list):
        ai_response = self.ai.Recommendation(task_list)
        self.lbl_ai_recomendation.after(0, lambda: UIStyle.apply_label_style(self.lbl_ai_recomendation, text=ai_response, font="body", max_width=500))


    def launch_list_view(self):
        self.show_frame("list_view")

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def getuser(self):
        return



root = tk.Tk()
app = TimeManager(root)
root.mainloop()