from my_parser import parse
from ast_to_string import ast_to_string
from merge_function import merge_function

import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont  # Import the font module

def switch_to_clear():
    # Update button text to "CLEAR"
    button_canvas.itemconfig(button_text, text="CLEAR")
    # Rebind button to clear function
    button_canvas.tag_bind(rounded_button, "<ButtonPress-1>", lambda x: on_clear_click())
    button_canvas.tag_bind(button_text, "<ButtonPress-1>", lambda x: on_clear_click())

def switch_to_merge():
    # Update button text to "MERGE"
    button_canvas.itemconfig(button_text, text="MERGE")
    # Rebind button to merge function
    button_canvas.tag_bind(rounded_button, "<ButtonPress-1>", lambda x: on_merge_click())
    button_canvas.tag_bind(button_text, "<ButtonPress-1>", lambda x: on_merge_click())

def on_clear_click():
    # Clear the input fields and output label
    user1_entry.delete(0, tk.END)
    user2_entry.delete(0, tk.END)
    output_label.config(text="Output: Merged Formula", fg=text_color)
    error_label.config(text="")  # Clear any previous error message
    # Switch back to merge functionality
    switch_to_merge()

def on_merge_click():
    # Get the formula from both input fields
    user1_formula = user1_entry.get()
    user2_formula = user2_entry.get()

    try:
        # Merge the formulas and display the result
        merged_formula = merge_function(user1_formula, user2_formula)
        output_label.config(text="Output: " + merged_formula, fg="#00ff00")  # Green text for output
        switch_to_clear()  # Switch button to clear functionality
    except Exception as e:
        # Display error in red
        output_label.config(text="Error: " + str(e), fg="red")
        
def on_button_enter(e):
    button_canvas.itemconfig(rounded_button, fill="#ff6666")  # Lighter red when hovered

def on_button_leave(e):
    button_canvas.itemconfig(rounded_button, fill=button_color)  # Original color when not hovered

# Create the main window
root = tk.Tk()
root.title("CELLSTER: Local-First Excel Formula Merger")

# Set a larger font
large_font = tkfont.Font(family="Helvetica", size=18, weight="bold")

# Set the window size and position it in the center of the screen
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Define a color scheme
bg_color = "#000000"  # Black background
input_bg = "#333333"  # Darker grey input field
button_color = "#ff0000"  # Red button
text_color = "#ffffff"  # White text

# Set the background color
root.configure(background=bg_color)

# Function to create rounded rectangle
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Create entry for user1's formula
user1_label = tk.Label(root, text="Input: User 1 Formula", font=large_font, bg=bg_color, fg=text_color)
user1_label.pack(pady=20)
user1_entry = tk.Entry(root, font=large_font, width=20, bg=input_bg, fg="#ffff00", borderwidth=0)  # Yellow text for input
user1_entry.pack()

# Create entry for user2's formula
user2_label = tk.Label(root, text="Input: User 2 Formula", font=large_font, bg=bg_color, fg=text_color)
user2_label.pack(pady=20)
user2_entry = tk.Entry(root, font=large_font, width=20, bg=input_bg, fg="#ffff00", borderwidth=0)  # Yellow text for input
user2_entry.pack()

# Custom button with rounded corners
button_canvas = tk.Canvas(root, width=220, height=60, bg=bg_color, highlightthickness=0)
button_canvas.pack(pady=20)
rounded_button = create_rounded_rectangle(button_canvas, 10, 10, 210, 60, radius=20, fill=button_color)
button_text = button_canvas.create_text(110, 35, text="MERGE", fill="white", font=large_font)
button_canvas.tag_bind(rounded_button, "<ButtonPress-1>", lambda x: on_merge_click())
button_canvas.tag_bind(button_text, "<ButtonPress-1>", lambda x: on_merge_click())

# Bind hover effects
button_canvas.tag_bind(rounded_button, "<Enter>", on_button_enter)
button_canvas.tag_bind(rounded_button, "<Leave>", on_button_leave)
button_canvas.tag_bind(button_text, "<Enter>", on_button_enter)
button_canvas.tag_bind(button_text, "<Leave>", on_button_leave)

# Create the output label
output_label = tk.Label(root, text="Output: Merged Formula", font=large_font, bg=bg_color, fg=text_color)
output_label.pack(pady=20)

# Create an error label
error_label = tk.Label(root, text="", font=large_font, bg=bg_color, fg="red")  # Empty initially
error_label.pack(pady=10)

# Start the application
root.mainloop()
