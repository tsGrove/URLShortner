from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import URLModel
from schemas import URLSchema

blp = Blueprint("URLs", "urls", description='Operations on urls')

@blp.route("/add-url")
class URLs(MethodView):
    @blp.arguments(URLSchema)
    @blp.response(201, URLSchema)
    def post(self, url_data):

        url = URLModel(**url_data)

        try:
            db.session.add(url)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(e, message=f"{url_data}")

        return url, 201

@blp.route("/all-urls")
class URLsList(MethodView):
    @blp.response(200, URLSchema(many=True))
    def get(self):

        return URLModel.query.all()

@blp.route("/<int:url_id>")
class URLInfo(MethodView):
    @blp.response(200, URLSchema)
    def get(self, url_id):
        url = URLModel.query.get_or_404(url_id)
        return url

    def delete(self, url_id):
        url = URLModel.query.get_or_404(url_id)
        db.session.delete(url)
        db.session.commit()
        return {"message" : f"The url {url.original_url} has successfully been deleted."}