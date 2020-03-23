import uuid
import datetime

from app import db
from app.models import User


def add_user(data):
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data["email"],
            password=data["password"]
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            "status": "fail",
            "message": "User already exist"
        }
        return response_object, 409


def  get_all_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        
        user_data["email"] = user.email
        user_data["admin"] = user.admin
        user_data["id"] = user.public_id

        output.append(user_data)

    return output


def get_user(id):
    """ Only for decorator """
    return User.query.filter_by(id=id).first()


def generate_token(user):
    try:
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            "status": "success",
            "message": "Successfully registered.",
            "Authorization": auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": "Some error. Try again"
        }
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()
