from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db

from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that name already exists.")

        user = UserModel(
            username = user_data["username"],
            password = user_data["password"]
        )

        db.session.add(user)
        db.session.commit()

        return {"message":f"User {user.username} successfully added!"}, 201


@blp.route("/user/id/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User {user.username} deleted."}, 200

@blp.route("/users/all")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

@blp.route("/user/name/<string:username>")
class UserSearch(MethodView):
    @blp.response(200, UserSchema)
    def get(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return jsonify({ "message": "User could not be found" }), 404
    # if URLModel.query.filter(URLModel.custom_url == url_data["custom_url"]).first():