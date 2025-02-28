from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'AZBYCX'
todos = []

@app.route("/", methods=["GET", "POST"])
def todo():
    return render_template("template.html", todos=todos)

@app.route("/submit", methods=["POST"])
def submit():
    selected_action = request.form.get('action')
    todos.clear()
    try:
        with open('to_do.txt', 'r') as f:
            lines = f.readlines()
            for x in lines:
                l = x.split('-')
                todos.append(l[1].strip())
    except IOError:
        print("File does not exist. Creating a new file.")
        with open('to_do.txt', 'w') as f:
            pass
        
    print("The list of previous todos: ", todos)

    if selected_action == 'add':
        add_action = request.form.get("ADD")
        if add_action:
            todos.append(add_action)
        else:
            flash("Please enter a task to add.")
    
    elif selected_action == 'show':
        for index, item in enumerate(todos):
            line = f"{index+1}-{item}"
            print(line)
        return redirect(url_for('todo'))
    
    elif selected_action == 'edit':
        if not todos:
            flash("No works exist to be edited!")
        else:
            index_value = request.form.get("EDIT")
            new_todo = request.form.get("EDIT_ACTION")
            if index_value and new_todo:
                index_value = int(index_value) - 1
                if 0 <= index_value < len(todos):
                    todos[index_value] = new_todo
                else:
                    flash("Invalid task number for editing.")
            else:
                flash("Please enter the task number and new task for editing.")
    
    elif selected_action == 'complete':
        index_value = request.form.get("COMPLETE")
        if index_value:
            index_value = int(index_value) - 1
            if 0 <= index_value < len(todos):
                todos.pop(index_value)
            else:
                flash("Invalid task number for completion.")
        else:
            flash("Please enter the task number to complete.")
    
    elif selected_action == "Choose...":
        flash("Please choose an Action")

    with open('to_do.txt', 'w') as f:
        for index, item in enumerate(todos):
            line = f"{index+1}-{item}"
            f.write(line + '\n')
        print("Written to to_do.txt")

    return redirect(url_for('todo'))

# REST API Endpoints


@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify({"todos": todos})

@app.route("/api/todo", methods=["POST"])
def add_todo():
    data = request.json
    task = data.get("task")
    if task:
        todos.append(task)
        return jsonify({"message": "Task added successfully", "todos": todos}), 201
    return jsonify({"error": "Task content is missing"}), 400

@app.route("/api/todo/<int:index>", methods=["GET"])
def get_specific_todo(index):
    """ Retrieve a specific task by its index. """
    if 0 <= index < len(todos):
        return jsonify({"task": todos[index]})
    return jsonify({"error": "Invalid task index"}), 404

@app.route("/api/todo/<int:index>", methods=["PUT"])
def update_todo(index):
    data = request.json
    new_task = data.get("task")
    if 0 <= index < len(todos):
        todos[index] = new_task
        return jsonify({"message": "Task updated successfully", "todos": todos})
    return jsonify({"error": "Invalid task index"}), 404

@app.route("/api/todo/<int:index>", methods=["DELETE"])
def delete_todo(index):
    if 0 <= index < len(todos):
        todos.pop(index)
        return jsonify({"message": "Task deleted successfully", "todos": todos})
    return jsonify({"error": "Invalid task index"}), 404

if __name__ == "__main__":
    app.debug = True
    app.run()

