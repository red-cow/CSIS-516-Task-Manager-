import tkinter as tk
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
        if isinstance(widget, tk.Entry):
            widget.config(width=40, show="*")  # Width applies to Entry but not Text
            widget.insert(0, placeholder)
        elif isinstance(widget, tk.Text):
            widget.config(height=1, width=40)  # Height applies to Text
            widget.insert("1.0", placeholder)