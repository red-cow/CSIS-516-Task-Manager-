import tkinter as tk
class UIStyle:
    COLORS = {
        "bg": "#2C3E50",
        "fg": "#ECF0F1",
        "primary": "#27AE60",
        "secondary": "#2980B9",
        "danger": "#E74C3C", ##E74C3C
        "neutral": "#95A5A6",
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
        "calendar": ("Arial", 12)
    }

    @staticmethod
    def apply_label_style(widget, text="", font="heading"):
        widget.config(
            text=text,
            font=UIStyle.FONTS[font],
            bg=UIStyle.COLORS["bg"],
            fg=UIStyle.COLORS["fg"],
            padx=20,
            pady=10
        )

    @staticmethod
    def apply_calendar_style(calendar):
        calendar.config(
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
    @staticmethod
    def apply_button_style(widget, text="", command=None, bg="neutral"):
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
            command=command
        )

        # Change color on hover
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=default_bg))

    @staticmethod
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
        if isinstance(widget, tk.Entry):
            widget.config(width=width, show="*")  # Width applies to Entry but not Text
            widget.insert(0, placeholder)
        elif isinstance(widget, tk.Text):
            widget.config(height=height, width=width)  # Height applies to Text
            widget.insert("1.0", placeholder)