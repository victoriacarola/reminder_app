import time
import schedule
import threading
from plyer import notification
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Send notification
def task_reminder(task):
    notification.notify(
        title="📌 Task Reminder",
        message=task,
        timeout=10
    )
    print(f"[Reminder] {task} - {datetime.now().strftime('%H:%M:%S')}")

# Schedule tasks
def schedule_task(task, time_str, repeat="Daily"):
    try:
        if repeat == "Daily":
            schedule.every().day.at(time_str).do(task_reminder, task)
        elif repeat == "Weekly":
            schedule.every().monday.at(time_str).do(task_reminder, task)
        elif repeat == "Hourly":
            schedule.every().hour.at(":00").do(task_reminder, task)
        messagebox.showinfo("Task Scheduled", f"✔ '{task}' at {time_str} ({repeat})")
    except schedule.ScheduleValueError:
        messagebox.showerror("Invalid Time", "Use 24h format HH:MM")

# Scheduler in background
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start background scheduler
threading.Thread(target=run_scheduler, daemon=True).start()

# ----------------- GUI -----------------

root = tk.Tk()
root.title("📅 Task Reminder")
root.geometry("500x360")
root.configure(bg="#ecf0f3")
root.resizable(False, False)

# Fonts
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 10)

# Styling with ttk
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#ecf0f3", font=FONT_LABEL)
style.configure("TButton", font=FONT_LABEL, padding=6, relief="flat", background="#4CAF50", foreground="white")
style.map("TButton",
          background=[('active', '#45a049')],
          relief=[('pressed', 'flat')])

style.configure("TEntry", padding=6, relief="flat")
style.configure("TCombobox", padding=6, relief="flat", selectbackground="#ffffff", fieldbackground="#ffffff")

# Title
tk.Label(root, text="🌟 Task Reminder", font=FONT_TITLE, bg="#ecf0f3", fg="#333").pack(pady=15)

form_frame = tk.Frame(root, bg="#ecf0f3")
form_frame.pack(pady=10)

# Task
tk.Label(form_frame, text="Task Description").grid(row=0, column=0, sticky="w", padx=10)
task_entry = ttk.Entry(form_frame, width=50, font=FONT_ENTRY)
task_entry.grid(row=1, column=0, padx=10, pady=(0, 10))

# Time
tk.Label(form_frame, text="Time (HH:MM)").grid(row=2, column=0, sticky="w", padx=10)
time_entry = ttk.Entry(form_frame, width=20, font=FONT_ENTRY)
time_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

# Repeat
tk.Label(form_frame, text="Repeat").grid(row=4, column=0, sticky="w", padx=10)
repeat_var = tk.StringVar(value="Daily")
repeat_box = ttk.Combobox(form_frame, textvariable=repeat_var, values=["Daily", "Weekly", "Hourly"],
                          width=18, state="readonly", font=FONT_ENTRY)
repeat_box.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="w")

# Add Task
def add_task():
    task = task_entry.get().strip()
    time_str = time_entry.get().strip()
    repeat = repeat_var.get()
    if task and time_str:
        schedule_task(task, time_str, repeat)
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Missing Info", "Enter both task and time.")

# View Tasks
def view_tasks():
    if not schedule.jobs:
        messagebox.showinfo("Scheduled Tasks", "No tasks scheduled.")
    else:
        tasks = "\n".join([f"{i+1}. {job.job_func.args[0]} at {job.at_time}" for i, job in enumerate(schedule.jobs)])
        messagebox.showinfo("Scheduled Tasks", tasks)

# Button frame
btn_frame = tk.Frame(root, bg="#ecf0f3")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Schedule Task", command=add_task).grid(row=0, column=0, padx=15)
ttk.Button(btn_frame, text="View Tasks", command=view_tasks).grid(row=0, column=1, padx=15)


# Start app
root.mainloop()
