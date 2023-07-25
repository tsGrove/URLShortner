from main.db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(14), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    url_info = db.relationship("URLModel", back_populates="user", lazy="dynamic")


