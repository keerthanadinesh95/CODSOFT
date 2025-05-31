
import tkinter as tk

# Function to update the expression
def button_click(number):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(number))

# Function to clear the entry
def clear_entry():
    entry.delete(0, tk.END)
    result_label.config(text="")  # Clear result label too

# Function to evaluate the expression
def calculate():
    expression = entry.get()
    try:
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
        result_label.config(text=f"{expression} = {result}")
    except Exception as e:
        entry.delete(0, tk.END)
        result_label.config(text="Error")

# Create main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("320x430")
root.resizable(False, False)

# Entry field
entry = tk.Entry(root, width=16, font=("Arial", 24), borderwidth=2, relief="solid", justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Result display label
result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
result_label.grid(row=1, column=0, columnspan=4)

# Button layout
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('+', 5, 2), ('=', 5, 3),
    ('Clear', 6, 0)
]

# Create and place buttons
for (text, row, col) in buttons:
    if text == '=':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 14),
                  command=calculate, bg='lightgreen').grid(row=row, column=col, padx=5, pady=5)
    elif text == 'Clear':
        tk.Button(root, text=text, width=23, height=2, font=("Arial", 14),
                  command=clear_entry, bg='lightcoral').grid(row=row, column=col, columnspan=4, padx=5, pady=5)
    else:
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 14),
                  command=lambda t=text: button_click(t)).grid(row=row, column=col, padx=5, pady=5)

# Run the application
root.mainloop()
