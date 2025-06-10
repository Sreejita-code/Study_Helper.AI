import json
import os
from datetime import datetime

TASKS_FILE = "data/tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(title, due_time=None):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "due_time": due_time  # Format: "YYYY-MM-DD HH:MM"
    }
    tasks.append(task)
    save_tasks(tasks)

def list_tasks():
    return load_tasks()

def delete_task(task_id):
    tasks = load_tasks()
    updated = [t for t in tasks if t["id"] != task_id]
    save_tasks(updated)

def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            break
    save_tasks(tasks)

def get_due_tasks():
    now = datetime.now()
    due = []
    for task in load_tasks():
        if task["due_time"] and not task["done"]:
            task_time = datetime.strptime(task["due_time"], "%Y-%m-%d %H:%M")
            if now >= task_time:
                due.append(task)
    return due