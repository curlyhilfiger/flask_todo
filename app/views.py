from flask import request, jsonify

from app.services import user_service
from app.services import todo_service
from app.services.auth_helper import Auth
from app.utils.decorator import token_required, admin_token_required

from app import app


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.get_json()
        return Auth.login_user(data)

@app.route("/users", methods=["GET"])
@admin_token_required
def get_users():
    
    try:
        users = user_service.get_all_users()
        return {"users": users}, 200
    except Exception as e:
        return {"error": e}, 404


@app.route("/user", methods=["POST"])
@admin_token_required
def create_user():
    if request.is_json:
        data = request.get_json()
        response = user_service.add_user(data)
        return response
    else:
        return {"error": "is not json"}


@app.route("/todos", methods=["GET"])
@token_required
def todos(current_user):

    response = todo_service.get_todos(current_user)
    return response
   

@app.route("/todo/<id>", methods=["GET"])
@token_required
def todo(current_user, id):

    response = todo_service.get_todo(current_user, id)
    return response


@app.route("/todo/<id>", methods=["DELETE"])
@token_required
def delete(current_user, id):

    response = todo_service.delete_todo(current_user, id)
    return response


@app.route("/edit/<id>", methods=["PUT"])
@token_required
def edit(current_user, id):

    if request.is_json:
        data = request.get_json()
        if "text" in data:
            response = todo_service.edit_todo(current_user, id, data["text"])
            return response

        response_object = {
            "status": "fail",
            "message": "No text attr"
        }

        return response_object, 404
        
    return {"error": "is not json"}


@app.route("/create", methods=["POST"])
@token_required
def create(current_user):

    if request.is_json:
        data = request.get_json()
        if "text" in data:
            response = todo_service.create_todo(current_user, data["text"])
            return response
        
        response_object = {
            "status": "fail",
            "message": "No text attr"
        }

        return response_object, 404

    return {"error": "is not json"}, 418

@app.route("/complete/<id>", methods=["PUT"])
@token_required
def complete(current_user, id):

    response = todo_service.complete_todo(current_user, id)
    return response
    