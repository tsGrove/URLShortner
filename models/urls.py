from db import db

class URLModel(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(), nullable=False)
    short_url = db.Column(db.String(), unique=True, nullable=False)
    searchable_short_url = db.Column(db.String(), unique=True, nullable=False)
    custom_url = db.Column(db.String(), nullable=True, default='')
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="url_info")

