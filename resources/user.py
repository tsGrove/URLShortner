from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")

# Registers the user in the database using a username and password provided by the user. A query is run to ensure that
# The username provided does not already exist in the database, the password is then hashed using the passlib library
# and added into the database alongside the username.
@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that name already exists.")

        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message":f"User {user.username} successfully added!"}, 201

# User provides a username and password, the password is then ran through the passlib library and if it matches with
# What the database has stored the user is successfully logged in and provided an access token and a refresh tokens for
# The end points which require one.
@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token" : access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid username and/or password.")

@blp.route("/user/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token":new_token}

# Takes the "jti" (JWT ID) and adds that to the blocklist set, preventing for a token being reused and ensuring a
# Unique token for each user.
@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200

# The user provides a user_id and is returned info about the user, including "username", and all urls associated with
# The user.
@blp.route("/user/id/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

# Deletes a user from the database.
    @jwt_required(fresh=True)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User {user.username} deleted."}, 200

# Returns a list of all users in the database.
@blp.route("/users/all")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

# Functions similarly to the user_id search except that this search allows the user of usernames instead of user_ids.
@blp.route("/user/name/<string:username>")
class UserSearch(MethodView):
    @blp.response(200, UserSchema)
    def get(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return jsonify({ "message": "User could not be found" }), 404