import tkinter as tk
from tkinter import StringVar

def submit():
    camera_link = link_entry.get()
    user_name = nickname_entry.get()
    exercise = exercise_var.get()

    print(f"Camera Link: {camera_link}")
    print(f"User Name: {user_name}")
    print(f"Selected Exercise: {exercise}")

# Create main window
root = tk.Tk()
root.title("Custom Interface")
root.geometry("400x300")
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# White circle
canvas.create_oval(200, -50, 800, 500, fill='white', outline='white')

# Creating the lines and shapes for the entries and button
canvas.create_line(150, 100, 250, 100, fill='white', width=30, capstyle='round')
canvas.create_line(150, 150, 250, 150, fill='white', width=30, capstyle='round')
canvas.create_line(150, 200, 250, 200, fill='white', width=30, capstyle='round')

# Nickname Entry
nickname_entry = tk.Entry(root, bg='white', fg='black', bd=0, highlightthickness=0, width=15)
nickname_entry_window = canvas.create_window(150, 100, anchor='w', window=nickname_entry)
canvas.create_text(80, 100, text="Nickname", fill='white', anchor='e')

# Link Entry
link_entry = tk.Entry(root, bg='white', fg='black', bd=0, highlightthickness=0, width=15)
link_entry_window = canvas.create_window(150, 150, anchor='w', window=link_entry)
canvas.create_text(80, 150, text="Link", fill='white', anchor='e')

# Exercise Selection
canvas.create_text(80, 200, text="Exercise", fill='white', anchor='e')

exercise_var = StringVar(root)
exercise_var.set("Squat")  # Default exercise selection

# Create a frame to contain the OptionMenu and style it like the entries
exercise_frame = tk.Frame(root, bg='white', bd=0, highlightthickness=0)
exercise_frame_window = canvas.create_window(150, 200, anchor='w', window=exercise_frame)

exercise_option = tk.OptionMenu(exercise_frame, exercise_var, "Squat", "Pushups", "Bicep Curl")
exercise_option.config(bg='white', fg='black', font=('Arial', 12), bd=0, highlightthickness=0, activebackground='white', activeforeground='black')
exercise_option['menu'].config(bg='white', fg='black', font=('Arial', 12))
exercise_option.pack(fill='both', expand=True)

# Submit Button
canvas.create_line(150, 250, 250, 250, fill='black', width=30, capstyle='round')
submit_button = tk.Label(root, text="Submit", bg='black', fg='white', font=('Arial', 12), cursor="hand2")
submit_button_window = canvas.create_window(200, 250, anchor='w', window=submit_button)

# Bind the submit function to the label to make it act like a button
submit_button.bind("<Button-1>", lambda e: submit())

root.mainloop()
