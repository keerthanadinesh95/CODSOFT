import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def generate_password():
    try:
        total_length = int(length_entry.get())
        num_letters = int(letters_entry.get() or 0)
        num_digits = int(digits_entry.get() or 0)
        num_special = int(special_entry.get() or 0)
        custom_word = word_entry.get()
        word_position = word_position_var.get()

        custom_word_length = len(custom_word)

        if num_letters or num_digits or num_special or custom_word:
            advanced_sum = num_letters + num_digits + num_special + custom_word_length
            if advanced_sum != total_length:
                messagebox.showerror(
                    "Length Mismatch",
                    f"Total specified length is {total_length}, but sum of inputs is {advanced_sum}. Please match them."
                )
                return

        remaining = total_length - (num_letters + num_digits + num_special + custom_word_length)
        characters = []
        characters += random.choices(string.ascii_letters, k=num_letters)
        characters += random.choices(string.digits, k=num_digits)
        characters += random.choices(string.punctuation, k=num_special)

        all_chars = string.ascii_letters + string.digits + string.punctuation
        characters += random.choices(all_chars, k=remaining)

        random.shuffle(characters)

        if word_position == "start":
            password = custom_word + ''.join(characters)
        elif word_position == "middle":
            mid = len(characters) // 2
            password = ''.join(characters[:mid]) + custom_word + ''.join(characters[mid:])
        else:  # end
            password = ''.join(characters) + custom_word

        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def copy_to_clipboard():
    password = result_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def clear_fields():
    length_entry.delete(0, tk.END)
    letters_entry.delete(0, tk.END)
    digits_entry.delete(0, tk.END)
    special_entry.delete(0, tk.END)
    word_entry.delete(0, tk.END)
    result_entry.delete(0, tk.END)
    word_position_var.set("end")

# GUI Setup
window = tk.Tk()
window.title("🔒 Advanced Password Generator")
window.geometry("500x530")
window.configure(bg="white")

tk.Label(window, text="🔐 Advanced Password Generator", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

tk.Label(window, text="Total Password Length:", bg="white", font=("Arial", 12)).pack()
length_entry = tk.Entry(window, font=("Arial", 12), justify="center")
length_entry.pack()

# Advanced Options Frame
options_frame = tk.LabelFrame(window, text="Advanced Options (Optional)", padx=10, pady=10, bg="white", font=("Arial", 10, "bold"))
options_frame.pack(pady=10)

tk.Label(options_frame, text="Number of Letters:", bg="white").grid(row=0, column=0, sticky="w")
letters_entry = tk.Entry(options_frame, width=5)
letters_entry.grid(row=0, column=1)

tk.Label(options_frame, text="Number of Digits:", bg="white").grid(row=1, column=0, sticky="w")
digits_entry = tk.Entry(options_frame, width=5)
digits_entry.grid(row=1, column=1)

tk.Label(options_frame, text="Number of Special Characters:", bg="white").grid(row=2, column=0, sticky="w")
special_entry = tk.Entry(options_frame, width=5)
special_entry.grid(row=2, column=1)

tk.Label(options_frame, text="Include Name/Word:", bg="white").grid(row=3, column=0, sticky="w")
word_entry = tk.Entry(options_frame)
word_entry.grid(row=3, column=1)

# Word placement radio buttons
tk.Label(options_frame, text="Position of Word:", bg="white").grid(row=4, column=0, sticky="w")
word_position_var = tk.StringVar(value="end")
tk.Radiobutton(options_frame, text="Start", variable=word_position_var, value="start", bg="white").grid(row=4, column=1, sticky="w")
tk.Radiobutton(options_frame, text="Middle", variable=word_position_var, value="middle", bg="white").grid(row=5, column=1, sticky="w")
tk.Radiobutton(options_frame, text="End", variable=word_position_var, value="end", bg="white").grid(row=6, column=1, sticky="w")

# Generate & Copy Buttons
tk.Button(window, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
result_entry = tk.Entry(window, font=("Courier", 14), justify="center", width=30)
result_entry.pack(pady=10)

# Copy and Clear Buttons
button_frame = tk.Frame(window, bg="white")
button_frame.pack(pady=5)

tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Clear", command=clear_fields, bg="#f44336", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=10)

window.mainloop()
