import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            data = json.load(file)
            for task in data["pending"]:
                add_task_to_list(task["task"], task["priority"], completed=False)
            for task in data["completed"]:
                add_task_to_list(task["task"], task["priority"], completed=True)

# Save tasks to JSON file
def save_tasks():
    pending = []
    completed = []
    for i in range(pending_listbox.size()):
        task, priority = pending_listbox.get(i).split(" [")[0], get_priority_from_text(pending_listbox.get(i))
        pending.append({"task": task, "priority": priority})
    for i in range(completed_listbox.size()):
        task, priority = completed_listbox.get(i).split(" [")[0], get_priority_from_text(completed_listbox.get(i))
        completed.append({"task": task, "priority": priority})

    with open(TASK_FILE, "w") as file:
        json.dump({"pending": pending, "completed": completed}, file)

# Helper to get priority from formatted text
def get_priority_from_text(text):
    return text.split("[")[-1].replace("]", "").strip()

# Add task to the appropriate list
def add_task_to_list(task, priority, completed=False):
    display_text = f"{task} [{priority}]"
    color = priority_colors[priority]
    if completed:
        completed_listbox.insert(tk.END, display_text)
        completed_listbox.itemconfig(tk.END, {'fg': color})
    else:
        pending_listbox.insert(tk.END, display_text)
        pending_listbox.itemconfig(tk.END, {'fg': color})

# Add a new task
def add_task():
    task = task_entry.get().strip()
    priority = priority_var.get()
    if task:
        add_task_to_list(task, priority)
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Delete selected task
def delete_task():
    if pending_listbox.curselection():
        pending_listbox.delete(pending_listbox.curselection()[0])
    elif completed_listbox.curselection():
        completed_listbox.delete(completed_listbox.curselection()[0])
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")
    save_tasks()

# Mark task as completed
def mark_completed():
    try:
        selected_index = pending_listbox.curselection()[0]
        task_text = pending_listbox.get(selected_index)
        pending_listbox.delete(selected_index)
        task, priority = task_text.split(" [")[0], get_priority_from_text(task_text)
        add_task_to_list(task, priority, completed=True)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

# Edit a task
def edit_task():
    try:
        selected_index = pending_listbox.curselection()[0]
        task_text = pending_listbox.get(selected_index)
        current_task = task_text.split(" [")[0]
        current_priority = get_priority_from_text(task_text)

        new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_task)
        if new_task:
            pending_listbox.delete(selected_index)
            add_task_to_list(new_task.strip(), current_priority, completed=False)
            save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

# ---------- UI Setup ----------
root = tk.Tk()
root.title("To-Do List with Priority")
root.geometry("700x500")
root.configure(bg='lightgray')

# Priority colors
priority_colors = {
    "High": "red",
    "Medium": "orange",
    "Low": "green"
}

# Task input frame
input_frame = tk.Frame(root, bg='lightgray')
input_frame.pack(pady=10)

tk.Label(input_frame, text="Task:", font=("Helvetica", 12), bg='lightgray').grid(row=0, column=0, padx=5)
task_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=30)
task_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Priority:", font=("Helvetica", 12), bg='lightgray').grid(row=0, column=2, padx=5)
priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(input_frame, priority_var, "High", "Medium", "Low")
priority_menu.grid(row=0, column=3, padx=5)

add_button = tk.Button(root, text="Add Task", font=("Helvetica", 12), command=add_task, bg="lightblue")
add_button.pack(pady=5)

# Columns for pending and completed tasks
columns_frame = tk.Frame(root, bg='lightgray')
columns_frame.pack(pady=10)

# Pending tasks
tk.Label(columns_frame, text="Pending Tasks", font=("Helvetica", 14, "bold"), bg='lightgray').grid(row=0, column=0)
pending_listbox = tk.Listbox(columns_frame, width=40, height=15, font=("Helvetica", 12), bd=2, relief="solid")
pending_listbox.grid(row=1, column=0, padx=10)

# Completed tasks
tk.Label(columns_frame, text="Completed Tasks", font=("Helvetica", 14, "bold"), bg='lightgray').grid(row=0, column=1)
completed_listbox = tk.Listbox(columns_frame, width=40, height=15, font=("Helvetica", 12), bd=2, relief="solid")
completed_listbox.grid(row=1, column=1, padx=10)

# Control buttons
button_frame = tk.Frame(root, bg='lightgray')
button_frame.pack(pady=15)

tk.Button(button_frame, text="Delete Task", width=15, command=delete_task, font=("Helvetica", 12), bg='red').grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Mark Completed", width=15, command=mark_completed, font=("Helvetica", 12), bg='green').grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Edit Task", width=15, command=edit_task, font=("Helvetica", 12), bg='orange').grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Save", width=15, command=save_tasks, font=("Helvetica", 12), bg='gray').grid(row=0, column=3, padx=10)

# Load tasks when app starts
load_tasks()

root.mainloop()
