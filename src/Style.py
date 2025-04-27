import tkinter as tk
from tkinter import ttk
class UIStyle:
    COLORS = { #list of colors used within the app
        "bg": "#2C3E50",
        "fg": "#ECF0F1",
        "primary": "#27AE60", #Green
        "secondary": "#2980B9",
        "danger": "#E74C3C", #Red
        "neutral": "#95A5A6", #Gery
        "input_bg": "#FFFFFF",
        "input_fg": "#333333",
        "border": "#BDC3C7",
        "calendar_bg": "#34495E",
        "calendar_header_bg": "#2C3E50",
        "calendar_selected_bg": "#E74C3C",
        "calendar_border": "#1ABC9C"

    }

    FONTS = {
        "heading": ("Helvetica", 20, "bold"),
        "subheading": ("Helvetica", 16, "bold"),
        "body": ("Helvetica", 12),
        "button": ("Helvetica", 12, "bold"),
        "input": ("Helvetica", 12),
        "calendar": ("Arial", 12),
        "small": ("Helvetica", 6)
    }

    @staticmethod # used to style labels
    def apply_label_style(widget, text="", font="heading", max_width=None):
        config = { #changes color and style to be in line with the app
            "text": text,
            "font": UIStyle.FONTS[font],
            "bg": UIStyle.COLORS["bg"],
            "fg": UIStyle.COLORS["fg"],
            "padx": 20,
            "pady": 10
        }
        if max_width is not None: # give a max width if provide
            config["wraplength"] = max_width #mainly used if we want to confine the size of a label for word warpping
        widget.config(**config)

    @staticmethod # used to style calendars
    def apply_calendar_style(calendar):
        calendar.config( # changes all the colors to be in theme with the app
            background=UIStyle.COLORS["calendar_bg"],
            foreground="white",
            headersbackground=UIStyle.COLORS["calendar_header_bg"],
            headersforeground="white",
            bordercolor=UIStyle.COLORS["calendar_border"],
            selectbackground=UIStyle.COLORS["calendar_selected_bg"],
            selectforeground="white",
            normalbackground=UIStyle.COLORS["calendar_bg"],
            normalforeground="white",
            weekendbackground=UIStyle.COLORS["calendar_bg"],
            weekendforeground="white",
            font=UIStyle.FONTS["calendar"],
            locale="en_US"
        )
    @staticmethod  # used to style buttons
    def apply_button_style(widget, text="", command=None, bg="neutral", width=10, height=1):
        default_bg = UIStyle.COLORS[bg]  # Store default background color
        hover_bg = "#5D6D7E"  # Slightly darker shade for hover effect

        widget.config(
            text=text,
            font=UIStyle.FONTS["button"],
            bg=default_bg,
            fg="white",
            activebackground=default_bg,  # Match normal background
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            command=command,
            width=width,  # Set width if provided
            height=height  # Set height if provided
        )

        # Change color on hover
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=default_bg))

    @staticmethod # used for styling a text or entry
    def apply_entry_style(widget, placeholder="", width = 40, height = 1):
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
        if isinstance(widget, tk.Entry): # Sees weather it's a text or entry widget
            widget.config(width=width, show="*")  # Width applies to Entry but not Text
            widget.insert(0, placeholder)
        elif isinstance(widget, tk.Text):
            widget.config(height=height, width=width)  # Height applies to Text
            widget.insert("1.0", placeholder)

    @staticmethod #styles comboboxes to fit the app
    def apply_combobox_style(widget, textvar, width=12, bg="neutral"):
        style =ttk.Style()

        style_name = f"{bg}.TCombobox" # style name

        default_bg = UIStyle.COLORS[bg]

        # Configure style
        style.configure(
            style_name,
            font=UIStyle.FONTS["body"],
            fieldbackground=default_bg,
            background=default_bg,
            foreground="white",
            padding=5
        )

        # Apply style to the combobox
        widget.config(
            width=width,
            style=style_name,
            textvariable=textvar
        )
