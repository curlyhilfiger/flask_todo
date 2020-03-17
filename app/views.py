from flask import request, jsonify

from app.services import (get_todos, create_todo, 
    get_todo, delete_todo, complete_todo, edit_todo)

from app import app



@app.route("/todos", methods=["GET"])
def todos():

    todos = get_todos()
    if len(todos) == 0:
        return  {}, 204

    return {"todos": todos}

@app.route("/todo/<id>", methods=["GET"])
def todo(id):

    try:
        todo = get_todo(id)
    except  AttributeError as e:
        return {"error": str(e)}, 404
    
    return {"todo": todo}

@app.route("/todo/<id>", methods=["DELETE"])
def delete(id):

    try:
        delete_todo(id)
    except  AttributeError as e:
        return {"error": str(e)}, 404

    return {"msg": "Todo was deleted"}

@app.route("/edit/<id>", methods=["PUT"])
def edit(id):

    if request.is_json:
        data = request.get_json()
        if id == "null":
            return {"error": "No id"}, 422
        print(data["text"])
        if "text" in data:
            edit_todo(id, data["text"])
            return {"msg": "Todo was success edited"}
            
        return {"msg": "No text atr"}, 404
        
    return {"msg": "Error"}

@app.route("/create", methods=["POST"])
def create():

    if request.is_json:
        data = request.get_json()
        if "text" in data:
            create_todo(data["text"])
            return {"msg": "Todo was success created"}
        
        return {"msg": "No text atr"}, 404

    return {"msg": "Error"}

@app.route("/complete/<id>", methods=["PUT"])
def complete(id):

    try:
        complete_todo(id)
    except AttributeError as e:
        return {"error": str(e)}, 404
    
    return {"msg": "Todo was completed"}
