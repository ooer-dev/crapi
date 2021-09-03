from crapi.models import db


class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.BigInteger, index=True, nullable=False)

    trigger = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

    delete_trigger = db.Column(db.Boolean, nullable=False, default=False)
    dm_response = db.Column(db.Boolean, nullable=False, default=False)
    contains_anywhere = db.Column(db.Boolean, nullable=False, default=False)
    has_target = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Reaction %r>' % self.id
