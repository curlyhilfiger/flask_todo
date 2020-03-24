from app.models import Todo
from app import db


def get_todos(user):
    """ Get all todos """

    todos = Todo.query.filter_by(user_id=user.id)

    if todos:
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
        
        response_object = {
            "status": "success",
            "todos": output
        }
        return response_object, 200
    else:
        response_object = {
            "status": "fail",
            "message": "error"
        }
        return response_object, 404


def get_todo(user, todo_id):
    """ Get one todo """
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

        todo_data = {}
        todo_data["id"] = todo.id
        todo_data["text"] = todo.text
        todo_data["complete"] = todo.complete

        response_object = {
            "status": "success",
            "todo": todo_data
        }
        return response_object, 200

    except Exception as e:
        response_object = {
            "status": "fail",
            "message": str(e)
        }
        return response_object, 404


def edit_todo(user, todo_id, text):
    """ Edit todo text """
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

        todo.text = text
        db.session.commit()

        response_object = {
            "status": "success",
            "message": "Successfully edited."
        }

        return response_object, 201

    except Exception as e:
        response_object = {
            "status": "fail",
            "message": str(e)
        }  
        return response_object, 404 


def delete_todo(user, todo_id):
    """ Removes todo """

    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

        db.session.delete(todo)
        db.session.commit()

        response_object = {
            "status": "success",
            "message": "Successfully deleted."
        }

        return response_object, 200 

    except Exception as e:
        response_object = {
            "status": "fail",
            "message": str(e)
        }
        return response_object, 404


def create_todo(user, text):
    """ Create todo  """

    todo = Todo(text=text, user=user)
    db.session.add(todo)
    db.session.commit()

    response_object = {
        "status": "success",
        "message": "Succefully created"
    }

    return response_object, 201


def complete_todo(user, todo_id):
    """ Makes todo complete """
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()

        todo.complete = not todo.complete
        db.session.commit()
        
        response_object = {
            "status": "success",
            "message": "Succefully complete"
        }
        return response_object, 200
    
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": str(e)
        }
        return response_object, 404
