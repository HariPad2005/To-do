from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'AZBYCX'
todos = []
students = []

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

# In-memory database for students

# Get all students
@app.route("/get_students", methods=["GET"])
def get_students():
    return jsonify({"students": students})

# Add a new student
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    name = data.get("name")
    department = data.get("department")
    student_id = data.get("id")
    
    if name and department and student_id:
        student = {"name": name, "department": department, "id": student_id}
        students.append(student)
        return jsonify({"message": "Student added successfully", "students": students}), 201
    
    return jsonify({"error": "Missing student data"}), 400

# Get a specific student by ID
@app.route("/get_student/<int:student_id>", methods=["GET"])
def get_specific_student(student_id):
    """ Retrieve a specific student by their ID. """
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify({"student": student})
    return jsonify({"error": "Student not found"}), 404

# Update a specific student's information
@app.route("/update_student/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    name = data.get("name")
    department = data.get("department")
    
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        if name:
            student['name'] = name
        if department:
            student['department'] = department
        return jsonify({"message": "Student updated successfully", "students": students})
    
    return jsonify({"error": "Student not found"}), 404

# Delete a specific student by ID
@app.route("/delete_student/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        students.remove(student)
        return jsonify({"message": "Student deleted successfully", "students": students})
    
    return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.debug = True
    app.run()

