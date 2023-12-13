import tkinter as tk
from copy import deepcopy
from parser.parser import parse
from tkinter import font as tkfont  # import the font module

from crdt.apply_changes import apply_changes_to_ast
from crdt.ast_comparison import compare_asts
from crdt.merge import merge_ast

# import customtkinter


nord_colors = {
    "nord0": "#2E3440",
    "nord1": "#3B4252",
    "nord2": "#434C5E",
    "nord3": "#4C566A",
    "nord4": "#D8DEE9",
    "nord5": "#E5E9F0",
    "nord6": "#ECEFF4",
    "nord7": "#8FBCBB",
    "nord8": "#88C0D0",
    "nord9": "#81A1C1",
    "nord10": "#5E81AC",
    "nord11": "#BF616A",
    "nord12": "#D08770",
    "nord13": "#EBCB8B",
    "nord14": "#A3BE8C",
    "nord15": "#B48EAD",
}


def switch_to_clear():
    # update button text to "clear"
    button_canvas.itemconfig(button_text, text="clear")
    # rebind button to clear function
    button_canvas.tag_bind(rounded_button, "<Button-1>", lambda x: on_clear_click())
    button_canvas.tag_bind(button_text, "<Button-1>", lambda x: on_clear_click())


def switch_to_merge():
    # update button text to "merge"
    button_canvas.itemconfig(button_text, text="merge")
    # rebind button to merge function
    button_canvas.tag_bind(rounded_button, "<Button-1>", lambda x: on_merge_click())
    button_canvas.tag_bind(button_text, "<Button-1>", lambda x: on_merge_click())


def on_clear_click():
    # clear the input fields and output label
    user1_entry.delete(0, tk.END)
    user2_entry.delete(0, tk.END)
    user3_entry.delete(0, tk.END)
    output_label.config(text="", fg=text_color)
    error_label.config(text="")  # clear any previous error message
    # switch back to merge functionality
    switch_to_merge()


def crdt_merge_formula(original_ast_str, user1_ast_str, user2_ast_str):
    # Parse the formulas into ASTs
    original_ast = parse(original_ast_str)
    user1_original_ast = deepcopy(original_ast)
    user2_original_ast = deepcopy(original_ast)

    user1_modified_ast = parse(user1_ast_str)
    user2_modified_ast = parse(user2_ast_str)

    # Compare ASTs
    user1_changes = compare_asts(user1_original_ast, user1_modified_ast)
    user2_changes = compare_asts(user2_original_ast, user2_modified_ast)

    # Apply changes
    user1_new_ast, user1_new_nodes = apply_changes_to_ast(
        user1_original_ast, user1_changes, user_id="user_1"
    )
    user2_new_ast, user2_new_nodes = apply_changes_to_ast(
        user2_original_ast, user2_changes, user_id="user_2"
    )

    # Merge changes
    user1_merged_ast = merge_ast(user1_new_ast, user2_new_nodes)
    # user2_merged_ast = merge_ast(user2_new_ast, user1_new_nodes)

    return str(user1_merged_ast)


def on_merge_click():
    # get the formula from both input fields
    user1_formula = user1_entry.get()
    user2_formula = user2_entry.get()
    user3_formula = user3_entry.get()

    try:
        # Merge the formulas using CRDT logic
        merged_formula = crdt_merge_formula(user1_formula, user2_formula, user3_formula)
        merged_formula = str(merged_formula)
        # print(merged_formula)
        output_label.config(text="Merged Formula: " + str(merged_formula), fg="#a3be8c")

        switch_to_clear()  # Switch button to clear functionality
    except Exception as e:
        # Display error in red
        output_label.config(text="Error: " + str(e), fg="red")


# Hover colors for entry fields
entry_hover_bg = nord_colors["nord1"]  # Darker color for hover
entry_default_bg = nord_colors["nord3"]  # Default color


def on_entry_hover_enter(event, entry):
    entry.config(bg=entry_hover_bg)


def on_entry_hover_leave(event, entry):
    entry.config(bg=entry_default_bg)


def on_button_enter(e):
    button_canvas.itemconfig(rounded_button, fill="#788c66")  # lighter red when hovered


def on_button_leave(e):
    button_canvas.itemconfig(
        rounded_button, fill=button_color
    )  # original color when not hovered


# Example of a modern-styled button in tkinter
def on_button_hover(e, button, hover_color="#bf616a"):
    button.configure(bg=hover_color)


# create the main window
root = tk.Tk()
# root = cusomtkinter.CTk()
root.title("cellster: local-first excel formula merger")

# Create an invisible frame as a spacer

# set a larger font
large_font = tkfont.Font(family="open sans", size=16, weight="bold")
normal_font = tkfont.Font(family="open sans", size=14, weight="bold")


# set the window size and position it in the center of the screen
window_width = 700
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


# Set the background color and text color
bg_color = nord_colors["nord0"]  # Dark background
text_color = nord_colors["nord5"]  # Light text
button_color = nord_colors["nord10"]  # Blue button
input_bg = nord_colors["nord3"]  # Darker grey input field
output_color = nord_colors["nord14"]  # Green output text

# Style parameters
button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
button_fg = nord_colors["nord6"]
hover_bg = nord_colors["nord10"]

# set the background color
root.configure(background=bg_color)


# function to create rounded rectangle
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius,
        y1,
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1,
        x2,
        y1 + radius,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2,
        y2 - radius,
        x2,
        y2,
        x2 - radius,
        y2,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2,
        x1,
        y2 - radius,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
        x1,
        y1 + radius,
        x1,
        y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# Padding values
external_padding = 20
internal_padding_x = 10
internal_padding_y = 5


# Layout parameters
padx = 10
pady = 10
ipadx = internal_padding_x
ipady = internal_padding_y

# Set row and column configurations for better alignment and spacing
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=2)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)

# Create labels and entries for user1, user2, and user3
user1_label = tk.Label(
    root, text="Original Formula", font=large_font, bg=bg_color, fg=text_color
)
user1_label.grid(row=0, column=2, columnspan=1, padx=20, pady=(50, 20), sticky="ew")

user1_entry = tk.Entry(
    root,
    font=normal_font,
    width=20,
    bg=entry_default_bg,
    fg=nord_colors["nord5"],
    borderwidth=0,
)
user1_entry.grid(row=1, column=2, columnspan=1, padx=20, pady=10, sticky="ew")
user1_entry.bind("<Enter>", lambda e: on_entry_hover_enter(e, user1_entry))
user1_entry.bind("<Leave>", lambda e: on_entry_hover_leave(e, user1_entry))


# Create a Canvas widget for the line
line_canvas = tk.Canvas(
    root, height=1, bg=nord_colors["nord4"], bd=0, highlightthickness=0
)
line_canvas.grid(row=2, column=0, columnspan=6, sticky="ew")

# Draw a line across the canvas
line_canvas.create_line(
    0, 1, line_canvas.winfo_reqwidth(), 1, fill=nord_colors["nord4"]
)

user2_label = tk.Label(root, text="User 1", font=large_font, bg=bg_color, fg=text_color)
user2_label.grid(row=3, column=2, columnspan=1, padx=20, pady=10, sticky="ew")

user2_entry = tk.Entry(
    root,
    font=normal_font,
    width=20,
    bg=entry_default_bg,
    fg=nord_colors["nord5"],
    borderwidth=0,
)
user2_entry.grid(row=4, column=2, columnspan=1, padx=20, pady=10, sticky="ew")
user2_entry.bind("<Enter>", lambda e: on_entry_hover_enter(e, user2_entry))
user2_entry.bind("<Leave>", lambda e: on_entry_hover_leave(e, user2_entry))

# Create label and entry for user3
user3_label = tk.Label(root, text="User 2", font=large_font, bg=bg_color, fg=text_color)
user3_label.grid(row=5, column=2, columnspan=1, padx=20, pady=10, sticky="ew")

user3_entry = tk.Entry(
    root,
    font=normal_font,
    width=20,
    bg=entry_default_bg,
    fg=nord_colors["nord5"],
    borderwidth=0,
)
user3_entry.grid(row=6, column=2, columnspan=1, padx=20, pady=10, sticky="ew")
user3_entry.bind("<Enter>", lambda e: on_entry_hover_enter(e, user3_entry))
user3_entry.bind("<Leave>", lambda e: on_entry_hover_leave(e, user3_entry))

# custom button with rounded corners
button_canvas = tk.Canvas(root, width=220, height=60, bg=bg_color, highlightthickness=0)
button_canvas.grid(row=7, column=2, columnspan=1, pady=20)  # Span across 3 columns
rounded_button = create_rounded_rectangle(
    button_canvas, 10, 10, 210, 60, radius=20, fill=button_color
)
button_text = button_canvas.create_text(
    110, 35, text="merge", fill=text_color, font=large_font
)
button_canvas.tag_bind(rounded_button, "<Button-1>", lambda x: on_merge_click())
button_canvas.tag_bind(button_text, "<Button-1>", lambda x: on_merge_click())

# bind hover effects
button_canvas.tag_bind(rounded_button, "<Enter>", on_button_enter)
button_canvas.tag_bind(rounded_button, "<Leave>", on_button_leave)
button_canvas.tag_bind(button_text, "<Enter>", on_button_enter)
button_canvas.tag_bind(button_text, "<Leave>", on_button_leave)

# Grid layout for output label
output_label = tk.Label(root, font=large_font, bg=bg_color, fg=text_color)
output_label.grid(row=8, column=2, pady=20)  # Span across 3 columns

# Grid layout for error label
error_label = tk.Label(root, text="", font=large_font, bg=bg_color, fg="red")
error_label.grid(row=9, column=2, columnspan=3, pady=10)  # Span across 3 columns

# start the application
root.mainloop()
