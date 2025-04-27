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
        # set up the widow of the app
        self.root = root
        self.root.title("Time Manager")
        self.root.geometry("1000x900")
        self.root.resizable(False,False)

        # set up datebase connector and ai connector
        self.db = Database_Driver()
        self.ai = ChatGPT()

        self.user = ["","","",""]  # defines the user array of attributes
        # [0] = email
        # [1] = name
        # [2] = dob
        # [3] = password

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

        # center home screen
        self.frames["home"].grid_columnconfigure(0, weight=1)
        self.frames["home"].grid_columnconfigure(6, weight=1)

        # Welcome Label
        self.lbl_welcome = tk.Label(self.frames["home"])
        self.lbl_welcome.grid(row=1, column=1, columnspan=4, sticky="ew")

        # Shows to days date and time live
        self.lbl_date = tk.Label(self.frames["home"])
        self.lbl_date.grid(row =2, column=1, columnspan=4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_date)

        # Label that says AI's next thing to do
        self.lbl_whats_recommend = tk.Label(self.frames["home"])
        self.lbl_whats_recommend.grid(row=5, column=1, columnspan=4, sticky="ew")
        UIStyle.apply_label_style(self.lbl_whats_recommend, font="subheading", text="What to Do Next (AI Assisted)")

        # Label that will hold the ai generated text
        self.lbl_ai_recomendation = tk.Label(self.frames["home"])
        self.lbl_ai_recomendation.grid(row=6,column=1, columnspan=4,sticky="ew")
        UIStyle.apply_label_style(self.lbl_ai_recomendation, text="AI generating response....", font="body",max_width=500)

        # refrese button to get a new AI response
        self.btn_ai_response_refresh = tk.Button(self.frames["home"])
        self.btn_ai_response_refresh.grid(row=6,column=5,stick="ew")
        UIStyle.apply_button_style(self.btn_ai_response_refresh, text="🔄", command=lambda: self.users_recommendation(self.db.GetTaskList(self.user[0])), width =2)

        # button to open the calendar view frame
        self.btn_calandar_view = tk.Button(self.frames["home"], command=lambda: self.show_frame("calendar"))
        self.btn_calandar_view.grid(row=4, column=2, padx=10, pady=5)  # Add padding to space out buttons
        UIStyle.apply_button_style(self.btn_calandar_view, text="📅 Calendar View",width=12)

        # button to open the list view frame
        self.btn_list_view = tk.Button(self.frames["home"])
        self.btn_list_view.grid(row=4, column=4, padx=10, pady=5)  # Add padding for spacing
        UIStyle.apply_button_style(self.btn_list_view, text="📜 List View", command=self.launch_list_view, width=12)

        # button to show the list
        self.btn_create_task = tk.Button(self.frames["home"])
        self.btn_create_task.grid(row=4, column=3, padx=10, pady=5, sticky="ew")  # Add padding and make it expand
        UIStyle.apply_button_style(self.btn_create_task, "➕ Add Task", command=lambda: self.show_frame("create_task"), width=12)

        # button that logs a user out (clearing all their information) and takes them back to the login screen
        self.btn_logout = tk.Button(self.frames["home"])
        self.btn_logout.grid(row=7, column=3, padx=10, pady=10)  # Add extra padding for the logout button
        UIStyle.apply_button_style(self.btn_logout, text="🚶‍♂️ logout", command=self.logout, bg="danger", width=12)

        if getattr(sys, 'frozen', False): # determines if we are in exe file or pycharm
            # If running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_path = os.path.dirname(__file__)

        # icon of the app, must both be accessed and reformated
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

        # label for the description
        self.lbl_description = tk.Label(self.frames["create_task"])
        self.lbl_description.grid(row=3, column=1, columnspan=5, padx=10, pady=5, stick="ew")
        UIStyle.apply_label_style(self.lbl_description, text="Description", font="subheading")

        # textbox for the description
        self.txt_task_description = tk.Text(self.frames["create_task"])
        self.txt_task_description.grid(row=4, column=1, columnspan=5, padx=10, pady=5, sticky="ew")
        UIStyle.apply_entry_style(self.txt_task_description, height=20, width=80)

        # Create Task Button
        self.btn_create_new_task = tk.Button(self.frames["create_task"])
        self.btn_create_new_task.grid(row=5, column=2, columnspan=4, padx=10, pady=10)
        UIStyle.apply_button_style(self.btn_create_new_task, text="Create", command=self.create_task)

        # button to go back to the login screen
        self.btn_to_home = tk.Button(self.frames["create_task"])
        self.btn_to_home.grid(row=5, column=1)
        UIStyle.apply_button_style(self.btn_to_home, text="🔙 Back", bg="danger", command=lambda: self.show_frame("home"))

        # --- Login Screen () ---
        self.frames["login"].grid_columnconfigure(0, weight=1)
        self.frames["login"].grid_columnconfigure(1, weight=0)
        self.frames["login"].grid_columnconfigure(2, weight=0)
        self.frames["login"].grid_columnconfigure(3, weight=1)

        # Title, please enter your email and password
        self.lbl_login = tk.Label(self.frames["login"])
        self.lbl_login.grid(row=0, column=1, columnspan=2, pady=(20, 10), sticky ='nsew')
        UIStyle.apply_label_style(self.lbl_login, "Please enter your email and password")

        # Email
        self.lbl_email = tk.Label(self.frames["login"])
        self.lbl_email.grid(row=1, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_email, "Email:")

        # text box for email
        self.txt_email_ln = tk.Text(self.frames["login"], height=1, width=50)
        self.txt_email_ln.grid(row=1, column=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_email_ln.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_email_ln)

        # Password
        self.lbl_password = tk.Label(self.frames["login"])
        self.lbl_password.grid(row=2, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_password, text="Password:")

        # text box for password
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

        # text box for email
        self.txt_email_ca = tk.Text(self.frames["create_account"], height=1, width=40)
        self.txt_email_ca.grid(row=1, column=2, columnspan=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_email_ca.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_email_ca)

        # Name
        self.lbl_name = tk.Label(self.frames["create_account"])
        self.lbl_name.grid(row=2, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_name, text="Name:")

        # text box for entering someones name
        self.txt_name = tk.Text(self.frames["create_account"], height=1, width=40)
        self.txt_name.grid(row=2, column=2, columnspan=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_name.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_name)

        # Password
        self.lbl_password = tk.Label(self.frames["create_account"])
        self.lbl_password.grid(row=3, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_password, text="Password:")

        # text box for someone's password, this one hides the characters
        self.txt_password_ca = tk.Entry(self.frames["create_account"], show="*", width=40)
        self.txt_password_ca.grid(row=3, column=2, columnspan=2, sticky="w", padx=(5, 10), pady=5)
        self.txt_password_ca.bind("<Tab>", self.focus_next_widget)
        UIStyle.apply_entry_style(self.txt_password_ca)

        # Date of Birth
        self.lbl_dob = tk.Label(self.frames["create_account"])
        self.lbl_dob.grid(row=4, column=1, sticky="e", padx=(10, 5), pady=5)
        UIStyle.apply_label_style(self.lbl_dob, text="Birthday:")

        # calendar to select your date of birth
        self.date_dob_ca = Calendar(self.frames["create_account"], selectmode="day", date_pattern="yyyy-mm-dd",
                                    maxdate=datetime.today().date())
        self.date_dob_ca.grid(row=4, column=2, sticky="w", pady=10)
        UIStyle.apply_calendar_style(self.date_dob_ca)

        # Buttons for both creating a account and going back to the login screen
        self.btn_new_account = tk.Button(self.frames["create_account"])
        self.btn_new_account.grid(row=5, column=2, pady=(10, 5))
        UIStyle.apply_button_style(self.btn_new_account, "Create Account", command=self.create_account, bg='primary')

        self.btn_back = tk.Button(self.frames["create_account"])
        self.btn_back.grid(row=5, column=4, pady=(10, 5), sticky='w')
        UIStyle.apply_button_style(self.btn_back, text="Back To Login", command=self.logout, bg="danger")

        # Label letting users know there passwords must be at least 8 characters long
        self.lbl_password_req = tk.Label(self.frames["create_account"])
        self.lbl_password_req.grid(row=6, column=2, pady=(10, 5))
        UIStyle.apply_label_style(self.lbl_password_req, text="*Passwords must be at least 8 characters long*", font="body")

        # --- Calendar Frame (integrating TaskCalendarApp class) ---
        self.calendar_frame = TaskCalendarApp(self.frames["calendar"], self)  # Embed the TaskCalendarApp here

        # --- List View Frame (integrating TaskGallery class) ---
        self.list_view_frame = TaskGallery(self.frames["list_view"], self)  # Embed the TaskGallery here

        self.show_frame("login")
        self.update_time()

    # background tasks
    def update_time(self): #  updates the time on the home page live
        now = datetime.now()
        current_time = now.strftime("%B %d, %Y %I:%M %p")
        self.lbl_date.config(text=current_time)
        self.lbl_date.after(1000, self.update_time) # updates every minute

        # visibility functions
    def show_frame(self, frame_name): # my frame chainging funciton
        """Hide all frames and show only the selected one."""
        for frame in self.frames.values():
            frame.place_forget()  # Hide all frames
        self.frames[frame_name].place(relx=0, rely=0, relwidth=1, relheight=1)  # Show selected frame
        # needs to call the class for these 2 frames since they are done in a different py file
        if frame_name == "list_view":
                self.list_view_frame.main(self.frames["list_view"], self)
        if frame_name == "calendar":
                self.calendar_frame.main(self.frames["calendar"], self)


    # event handlers
    def login(self):  # logins users in if we can find them in the database
        if hasattr(self, 'lbl_login_fail'):  # deletes old failed login message if it exists
            self.lbl_login_fail.destroy()

        user_email = self.txt_email_ln.get("1.0", "end-1c").strip() # gets their email
        try:
            result = self.db.GetUser(user_email)  # try to get user from the database
            # checks to make sure we got a user and that the password matches what the user entered
            if result and result[3] == self.txt_password_ln.get():
                self.user = result  # save the result to the apps object
                print(self.user)
                UIStyle.apply_label_style(self.lbl_welcome, text=f"Welcome {self.user[1]}")  # says welcome with there name
                temp = self.db.GetTaskList(self.user[0])  # gets the users task
                threading.Thread(target=lambda: self.users_recommendation(temp), daemon=True).start()  # runs the ai recomendation
                self.show_frame("home")  # goes to the home screen
            else:
                self.show_login_fail_message()  # Now always executed if login fails
        except Exception as e:
            print(f"Error: {e}")  # Helps debug if something is wrong

    def create_account(self):
        if hasattr(self, 'lbl_create_account_fail'): # sees if we have a failed create account
            self.lbl_create_account_fail.destroy()
        # get users attributes from texts boxes
        name = self.txt_name.get("1.0", "end-1c")
        email = self.txt_email_ca.get("1.0", "end-1c")
        password = self.txt_password_ca.get()
        dob = self.date_dob_ca.get_date()
        # make sure both all text fields filled and that the password is over 8 charaters
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
                # creates a user and saves it's information
                result = self.db.CreateUser(email, name, dob, password)
                print(result)
                self.user = result  # saves it

                # clears out all the text fields
                self.txt_name.delete("1.0", "end")
                self.txt_email_ca.delete("1.0", "end")
                self.txt_password_ca.delete(0, "end")

                # does welcome with the users name
                UIStyle.apply_label_style(self.lbl_welcome, text=f"Welcome {self.user[1]}")

                # does the ai recommendation based on their tasks
                temp = self.db.GetTaskList(self.user[0])
                threading.Thread(target=lambda: self.users_recommendation(temp), daemon=True).start()

                self.show_frame("home")  # Shows home frame
            except Exception as e:
                print(e)

    def logout(self): # logs a users out
        # resests all textboxes and users attrubutes to blank
        self.user = ["","","",""]
        self.txt_email_ln.delete("1.0", "end")
        self.txt_password_ln.delete(0, "end")
        self.txt_email_ca.delete("1.0", "end")
        self.txt_name.delete("1.0", "end")
        self.txt_password_ca.delete(0, "end")
        # reset the getting AI recommendations to a default message
        UIStyle.apply_label_style(self.lbl_ai_recomendation, text="AI generating response....", font="body",
                                  max_width=500)  # removes the last users AI response to avoid confusion while the new one loads
        if hasattr(self, 'lbl_login_fail'):  # removes the login failed label if it exists
            self.lbl_login_fail.destroy()

        if hasattr(self, 'lbl_create_account_fail'):  # removes the crated account failed label if it exists
            self.lbl_create_account_fail.destroy()

        self.show_frame("login")  # goes back to login page

    def create_task(self):  # create a new task for the users
        try:
            date_text = self.date_label_task_created.cget("text")
            date_value = date_text.split(": ")[1] # substrings out the new date
            # creates a new task based on all the fields
            return_value = self.db.CreateTask(self.priority_var.get(), self.txt_task_description.get("1.0", "end-1c"), self.txt_task_title.get("1.0", "end-1c"), date_value,self.user[0])
            if not(return_value):  # sees that task was not successfully created
                tk.messagebox.showerror("Task not created", "Some fields were left blank")
            else:  # shows that task was created successfully created
                tk.messagebox.showinfo("Success", "Task Created Successfully")
                # clear out all fields
                self.txt_task_title.delete("1.0","end")
                self.txt_task_description.delete("1.0", "end")
                self.priority_dropdown.current(1)
                self.show_frame("home") # goes back to home page
        except Exception as e: # means some fields were left blank so sql code error out
            tk.messagebox.showerror("Task not created", "Some fields were left blank")


    def show_create_account_fail_message(self, password_not_over_8, empty_fields):
        if hasattr(self, 'lbl_create_account_fail'):
            self.lbl_create_account_fail.destroy()  # removes duplicate labels
        text = ""

        if len(empty_fields) != 0: # combines all the fields that were left blank
            text += f"You forgot to fill out field(s): {', '.join(empty_fields)}. "
            # if a password is over 8 character destroy the reminder says to keep passwords over 8 chars
        if not password_not_over_8:
            self.lbl_password_req.destroy()
        else: # if a password is not over 8 character add the reminder says to keep passwords over 8 chars
            self.lbl_password_req = tk.Label(self.frames["create_account"])
            self.lbl_password_req.grid(row=6, column=2, pady=(10, 5))
            UIStyle.apply_label_style(self.lbl_password_req, text="*Passwords must be at least 8 characters long*", font="body")

        self.lbl_create_account_fail = tk.Label(self.frames["create_account"], text= text, fg=UIStyle.COLORS["danger"], bg=UIStyle.COLORS["bg"])
        self.lbl_create_account_fail.grid(row=8, column=2, pady=(10, 5))

        self.root.update()  # Force UI refresh
    def show_login_fail_message(self):  # shows a message that the users failed to login
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()  # Prevents duplicate labels

        self.lbl_login_fail = tk.Label(self.frames["login"], text="Either password or username was incorrect", fg=UIStyle.COLORS["danger"], bg=UIStyle.COLORS["bg"])
        self.lbl_login_fail.grid(row=5, column=1, columnspan=2, pady=(20, 5))

        self.root.update()  # Force UI refresh

    def users_recommendation(self, task_list): # shows the ai response to a uses given list of task
        ai_response = self.ai.Recommendation(task_list)
        self.lbl_ai_recomendation.after(0, lambda: UIStyle.apply_label_style(self.lbl_ai_recomendation, text=ai_response, font="body", max_width=500))

    def launch_list_view(self):  # shows the list view frame
        self.show_frame("list_view")

    def focus_next_widget(self, event):  # allows you tab between widgets
        event.widget.tk_focusNext().focus()
        return "break"



root = tk.Tk()
app = TimeManager(root)
root.mainloop()