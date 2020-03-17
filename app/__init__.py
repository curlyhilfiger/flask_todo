from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


class MyResponse(Response):
    """ 
    With this class write {"key":"value"} in view,
    instead jsonify {"key":"value"}
    """
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(MyResponse, cls).force_type(rv, environ)

class MyFlask(Flask):
    response_class = MyResponse


app = MyFlask(__name__)
CORS(app)

if app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")

db = SQLAlchemy(app)

from app import views
from app import models
