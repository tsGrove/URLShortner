import random
import string
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify

from db import db
from models import URLModel
from schemas import PLainURLSchema

blp = Blueprint("URLs", "urls", description='Operations on urls')

@blp.route("/url/add-url")
class URLs(MethodView):
    @blp.arguments(PLainURLSchema)
    @blp.response(201, PLainURLSchema)
    def post(self, url_data):

        url = URLModel(**url_data)
        length = 8
        characters = string.ascii_letters + string.digits
        generated_string = ''.join(random.choices(characters, k=length))
        random_url = f"www.shorturl.com//{generated_string}"
        url.short_url = random_url

        if URLModel.query.filter(URLModel.custom_url == url_data["custom_url"]).first():
            abort(409, message="A custom URL with that name already exists.")


        try:
                db.session.add(url)
                db.session.commit()
        except SQLAlchemyError as e:
                abort(e, message=f"{url_data}")

        return url, 201

@blp.route("/url/all-urls")
class URLsList(MethodView):
    @blp.response(200, PLainURLSchema(many=True))
    def get(self):

        return URLModel.query.all()

@blp.route("/url/id/<int:url_id>")
class URLInfo(MethodView):
    @blp.response(200, PLainURLSchema)
    def get(self, url_id):
        url = URLModel.query.get_or_404(url_id)
        return url

    def delete(self, url_id):
        url = URLModel.query.get_or_404(url_id)
        db.session.delete(url)
        db.session.commit()
        return {"message" : f"The url {url.original_url} has successfully been deleted."}

@blp.route("/url/redirect/<string:short_url>")
class URLRedirection(MethodView):
    @blp.response(200, PLainURLSchema)
    def get(self, short_url):
        print("DICKS")
        url = URLModel.query.get_or_404(short_url)
        return {"original_url":url.short_url}
