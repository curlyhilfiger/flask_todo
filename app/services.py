from app.models import Todo
from app import db


def get_todos():
    """ Get all todos """

    todos = Todo.query.all()

    output = []

    for todo in todos:
        todo_data = {}
        todo_data["id"] = todo.id
        todo_data["text"] = todo.text
        todo_data["complete"] = todo.complete

        if todo.complete == True:
            output.append(todo_data)
            continue
        output.insert(0, todo_data)

    return output


def get_todo(todo_id):
    """ Get one todo """

    todo = Todo.query.filter_by(id=todo_id).first()

    todo_data = {}
    todo_data["id"] = todo.id
    todo_data["text"] = todo.text
    todo_data["complete"] = todo.complete

    return todo_data


def edit_todo(todo_id, text):
    """ Edit todo text """

    todo = Todo.query.filter_by(id=todo_id).first()

    todo.text = text
    db.session.commit()    


def delete_todo(todo_id):
    """ Removes todo """

    todo = Todo.query.filter_by(id=todo_id).first()

    db.session.delete(todo)
    db.session.commit()


def create_todo(text):
    """ Create todo  """

    todo = Todo(text=text)
    db.session.add(todo)
    db.session.commit()


def complete_todo(todo_id):
    """ Makes todo complete """

    todo = Todo.query.filter_by(id=todo_id).first()

    todo.complete = not todo.complete
    db.session.commit()
