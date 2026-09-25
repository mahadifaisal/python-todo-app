from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

TASKS_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    else:
        tasks = []

    # পুরোনো task-এ id না থাকলে id তৈরি করা
    changed = False

    for task in tasks:
        if "id" not in task:
            existing_ids = [
                t.get("id", 0)
                for t in tasks
                if isinstance(t.get("id", 0), int)
            ]

            task["id"] = max(existing_ids, default=0) + 1
            changed = True

    if changed:
        save_tasks(tasks)

    return tasks


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


@app.route("/")
def home():
    tasks = load_tasks()

    filter_type = request.args.get("filter", "all")

    if filter_type == "active":
        filtered_tasks = [
            task for task in tasks
            if not task["completed"]
        ]

    elif filter_type == "completed":
        filtered_tasks = [
            task for task in tasks
            if task["completed"]
        ]

    else:
        filtered_tasks = tasks

    total = len(tasks)
    completed = sum(
        1 for task in tasks
        if task["completed"]
    )
    active = total - completed

    return render_template(
        "index.html",
        tasks=filtered_tasks,
        total=total,
        active=active,
        completed=completed,
        current_filter=filter_type
    )


@app.route("/add", methods=["POST"])
def add_task():
    task_title = request.form.get("task", "").strip()

    if task_title:
        tasks = load_tasks()

        new_id = max(
            [task["id"] for task in tasks],
            default=0
        ) + 1

        tasks.append({
            "id": new_id,
            "title": task_title,
            "completed": False
        })

        save_tasks(tasks)

    return redirect("/")


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break

    save_tasks(tasks)

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()

    tasks = [
        task for task in tasks
        if task["id"] != task_id
    ]

    save_tasks(tasks)

    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    new_title = request.form.get("title", "").strip()

    if new_title:
        tasks = load_tasks()

        for task in tasks:
            if task["id"] == task_id:
                task["title"] = new_title
                break

        save_tasks(tasks)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)