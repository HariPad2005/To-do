from flask import Flask, render_template, request, redirect, url_for, flash

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

if __name__ == "__main__":
    app.debug = True
    app.run()
