from flask import *
from flask import render_template
app = Flask (__name__)
todos=[]
@app.route("/",methods=["GET","POST","DELETE"])
def todo():
    return render_template("template.html",todos=todos)    
@app.route("/submit",methods=["post"])
def submit():
    selected_action = request.form.get('action')
    todos.clear()
    try:
        with open('to_do.txt','r') as f:
            lines = f.readlines()
            for x in lines:
                l=x.split('-')
                todos.append(l[1].strip())
            f.close()
    except IOError:
            print("File doesnot exist. Creating a new file.")
            f=open('to_do.txt','w')                                #The File is created if it doesnot exist.
            f.close()
    print("The list of previous todo-s: ",todos)                    #previous works that are already stored.   
    if selected_action == 'add':
            add_action=request.form.get("ADD")
            todos.append(add_action)
            with open('to_do.txt','w') as f:
                for index, item in enumerate(todos):
                    line = f"{index+1}-{item}"
                    f.write(line+'\n')                          #written to file
            print("Written to to_do.txt")
    elif selected_action == 'show':
            for index, item in enumerate(todos):
                line = f"{index+1}-{item}"
                print(line)
            return redirect(url_for('todo'))
    elif selected_action == 'edit':
            if(len(todos)==0):                                  #if the list is empty, it prints there are no works existing.
                print("No works exist to be edited!")    
            print(todos)
            index_value = int(request.form.get("EDIT"))
            index_value -= 1
            new_todo = request.form.get("EDIT_ACTION")
            todos[index_value] = new_todo
            with open('to_do.txt','w') as f:
                for index, item in enumerate(todos):
                    line = f"{index+1}-{item}"
                    f.write(line+'\n')                          #written to file
            print("Written to to_do.txt")
    elif selected_action == 'complete':
            index_value = int(request.form.get("COMPLETE"))
            index_value -= 1
            todos.pop(index_value)
            with open('to_do.txt','w') as f:
                for index, item in enumerate(todos):
                    line = f"{index+1}-{item}"
                    f.write(line+'\n')                          #written to file
            print("Written to to_do.txt") 
           
    return redirect(url_for('todo'))
               
                         #if an invalid option is given, It notifies.'''


if __name__=="__main__":
    app.debug=True
    app.run()