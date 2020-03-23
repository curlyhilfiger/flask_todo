from functools import wraps

from flask import request

from app.services.auth_helper import Auth
from app.services import user_service


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get("data")

        if not token:
            return data, status

        user_id = token.get("user_id")
        current_user = user_service.get_user(user_id)

        return f(current_user, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get("data")

        if not token:
            return data, status

        admin = token.get("admin")
        if not admin:
            response_object = {
                "status": "fail",
                "message": "admin token required"
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
