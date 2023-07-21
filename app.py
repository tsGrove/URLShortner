from flask import Flask, jsonify, request, redirect
from flask_smorest import Api

from db import db
""" FOR LOGGING PURPOSES"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()

from resources.user import blp as UserBlueprint
from resources.urls import blp as URLBlueprint

def create_app(db_url=None):

    app = Flask(__name__)
    app.debug = True

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config["OPEN_URL_PREFIx"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = '/swagger-ui'
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(URLBlueprint)

    with app.app_context():
        db.create_all()

    return app