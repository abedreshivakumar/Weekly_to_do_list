from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
todo_list = {day: [] for day in week_days}

def load_tasks(filename="tasks.json"):
    global todo_list
    if os.path.exists(filename):
        with open(filename, "r") as file:
            todo_list = json.load(file)
    else:
        print("No saved tasks found.")

def save_tasks(filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(todo_list, file)

@app.route('/')
def index():
    load_tasks()
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add_task():
    day = request.form['day']
    task = request.form['task']
    priority = request.form['priority']
    if day in todo_list:
        todo_list[day].append({"task": task, "priority": priority, "status": "Not Started"})
        save_tasks()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_task():
    day = request.form['day']
    task_name = request.form['task_name']
    status = request.form['status']
    if day in todo_list:
        for task in todo_list[day]:
            if task['task'] == task_name:
                task['status'] = status
                break
        save_tasks()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
