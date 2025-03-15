class Show:
    @staticmethod
    def show_login(self):
        self.create_account_frame.grid_forget()
        self.home_frame.grid_forget()
        if hasattr(self, 'lbl_login_fail'):
            self.lbl_login_fail.destroy()

        self.login_frame.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def show_home(self):
        self.calendar_frame.grid_forget()
        self.login_frame.grid_forget()
        self.lbl_welcome.config(text=f"Hello, {self.user[1]}")
        self.home_frame.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def show_create_account(self):
        self.login_frame.grid_forget()
        self.create_account_frame.grid(row=0, column=0, sticky="nsew")