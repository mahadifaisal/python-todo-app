import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    return []


def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


tasks = load_tasks()


def show_tasks():
    if not tasks:
        print("\nNo tasks yet.")
        return

    print("\nYour Tasks:")

    for number, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else " "
        print(f"{number}. [{status}] {task['title']}")


def add_task():
    title = input("\nEnter a new task: ")

    if title.strip():
        tasks.append({
            "title": title,
            "completed": False
        })

        save_tasks()
        print("Task added successfully!")

    else:
        print("Task cannot be empty.")


def complete_task():
    show_tasks()

    if not tasks:
        return

    try:
        number = int(input("\nEnter task number to complete: "))

        if 1 <= number <= len(tasks):
            tasks[number - 1]["completed"] = True
            save_tasks()
            print("Task completed!")

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    show_tasks()

    if not tasks:
        return

    try:
        number = int(input("\nEnter task number to delete: "))

        if 1 <= number <= len(tasks):
            removed_task = tasks.pop(number - 1)
            save_tasks()
            print(f"Deleted: {removed_task['title']}")

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


while True:
    print("\n===== Python To-Do App =====")
    print("1. Show Tasks")
    print("2. Add Task")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        show_tasks()

    elif choice == "2":
        add_task()

    elif choice == "3":
        complete_task()

    elif choice == "4":
        delete_task()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")