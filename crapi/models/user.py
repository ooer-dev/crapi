from flask_login import UserMixin

from crapi.models import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.BigInteger, unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<User %r>' % self.username
