from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import key
import jwt


class BlacklistToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class User(db.Model):
    """ User model for storing user related things """
    __tablename__= "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String, unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    todos = db.relationship("Todo", backref="user")

    @property
    def password(self):
        raise AttributeError("password: write-only-field")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):

        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=15),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm="HS256"
            )
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):

        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            else:
                return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."      


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
