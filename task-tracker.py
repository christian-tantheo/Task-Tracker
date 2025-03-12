import os
import json
import sys
from datetime import datetime

# Constants
TASKS_FILE = "tasks.json"

# Ensure the JSON file exists
def initialize_tasks_file():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)

def load_tasks():
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def generate_task_id(tasks):
    return max([task['id'] for task in tasks], default=0) + 1

def add_task(description):
    tasks = load_tasks()
    task = {
        "id": generate_task_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully.")
            return
    print("Task not found.")

def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == len(updated_tasks):
        print("Task not found.")
    else:
        save_tasks(updated_tasks)
        print("Task deleted successfully.")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}.")
            return
    print("Task not found.")

def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = tasks if status is None else [task for task in tasks if task["status"] == status]
    if not filtered_tasks:
        print("No tasks found.")
        return
    for task in filtered_tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")

def main():
    initialize_tasks_file()
    args = sys.argv[1:]

    if not args:
        print("No command provided. Available commands: add, update, delete, mark-in-progress, mark-done, list")
        return

    command = args[0]

    if command == "add" and len(args) > 1:
        add_task(" ".join(args[1:]))
    elif command == "update" and len(args) > 2:
        try:
            update_task(int(args[1]), " ".join(args[2:]))
        except ValueError:
            print("Invalid task ID.")
    elif command == "delete" and len(args) > 1:
        try:
            delete_task(int(args[1]))
        except ValueError:
            print("Invalid task ID.")
    elif command == "mark-in-progress" and len(args) > 1:
        try:
            mark_task(int(args[1]), "in-progress")
        except ValueError:
            print("Invalid task ID.")
    elif command == "mark-done" and len(args) > 1:
        try:
            mark_task(int(args[1]), "done")
        except ValueError:
            print("Invalid task ID.")
    elif command == "list":
        if len(args) > 1 and args[1] in ["done", "todo", "in-progress"]:
            list_tasks(args[1])
        else:
            list_tasks()
    else:
        print("Invalid command or arguments. Available commands: add, update, delete, mark-in-progress, mark-done, list")

if __name__ == "__main__":
    main()