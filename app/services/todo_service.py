from app.models import Todo
from app import db


def get_todos(user):
    """ Get all todos """

    todos = Todo.query.filter_by(user_id=user.id)

    output = []

    for todo in todos:
        todo_data = {}
        todo_data["id"] = todo.id
        todo_data["text"] = todo.text
        todo_data["complete"] = todo.complete
        todo_data["user_id"] = todo.user_id

        if todo.complete == True:
            output.append(todo_data)
            continue
        output.insert(0, todo_data)

    return output


def get_todo(user, todo_id):
    """ Get one todo """

    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

    todo_data = {}
    todo_data["id"] = todo.id
    todo_data["text"] = todo.text
    todo_data["complete"] = todo.complete

    return todo_data


def edit_todo(user, todo_id, text):
    """ Edit todo text """

    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

    todo.text = text
    db.session.commit()    


def delete_todo(user, todo_id):
    """ Removes todo """

    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

    db.session.delete(todo)
    db.session.commit()


def create_todo(user, text):
    """ Create todo  """

    todo = Todo(text=text, user=user)
    db.session.add(todo)
    db.session.commit()


def complete_todo(user, todo_id):
    """ Makes todo complete """

    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

    todo.complete = not todo.complete
    db.session.commit()
