
from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "tasks.db")


# Create database and table
def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# HTML page
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Task Manager</title>
    <style>
        body {
            font-family: Arial;
            background: #eef2ff;
            text-align: center;
            padding: 40px;
        }

        .container {
            background: white;
            max-width: 500px;
            margin: auto;
            padding: 25px;
            border-radius: 12px;
        }

        input {
            padding: 10px;
            width: 65%;
        }

        button {
            padding: 10px;
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }

        li {
            margin: 15px;
        }

        .delete {
            background: #dc2626;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>Student Task Manager</h1>

    <form action="/add" method="POST">
        <input type="text" name="task"
               placeholder="Enter your task" required>
        <button type="submit">Add</button>
    </form>

    <h2>My Tasks</h2>

    <ul>
        {% for task in tasks %}
        <li>
            {{ task[1] }}

            <form action="/delete/{{ task[0] }}"
                  method="POST" style="display:inline">
                <button class="delete">Delete</button>
            </form>
        </li>
        {% endfor %}
    </ul>

</div>

</body>
</html>
"""


# Display all tasks
@app.route("/")
def home():

    conn = sqlite3.connect(DB_PATH)
    tasks = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return render_template_string(HTML, tasks=tasks)


# Add task
@app.route("/add", methods=["POST"])
def add_task():

    task = request.form.get("task", "").strip()

    if task:
        conn = sqlite3.connect(DB_PATH)

        conn.execute(
            "INSERT INTO tasks (task) VALUES (?)",
            (task,)
        )

        conn.commit()
        conn.close()

    return redirect("/")


# Delete task
@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":

    init_db()

    app.run(host="0.0.0.0", port=5000)
