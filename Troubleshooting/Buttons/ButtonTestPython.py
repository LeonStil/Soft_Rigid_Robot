import tkinter as tk

# This is the variable we want to change
value = 0

# Function to update the label text
def update_label():
    label.config(text=f"Value: {value}")

# Functions to change the variable and update the label
def add_one():
    global value # We need to declare 'value' as global to modify it inside the function
    value += 1 # Increment the value by 1
    update_label() # Update the label to reflect the new value

def subtract_one():
    global value
    value -= 1
    update_label()

# Create popup window
window = tk.Tk()
window.title("Variable Controller")
window.geometry("500x150")

# Text showing current value
label = tk.Label(window, text=f"Value: {value}", font=("Arial", 18))
label.pack(pady=20)

# Button frame
button_frame = tk.Frame(window)
button_frame.pack()

minus_button = tk.Button(button_frame, text="-1", width=8, command=subtract_one)
minus_button.pack(side="left", padx=10)

plus_button = tk.Button(button_frame, text="+1", width=8, command=add_one)
plus_button.pack(side="left", padx=10)

# Keep window open
window.mainloop()