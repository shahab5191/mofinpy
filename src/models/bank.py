from datetime import datetime
from src.extensions import db


class Bank(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40))
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime(), default=datetime.utcnow, onpdate=datetime.utcnow)
    author_id = db.Column(db.UUID(), db.ForeignKey('user.id'))

    # Relationships
    currency = db.relationship('Currency')
    author = db.relationship('User')

    def __init__(self, name, currency_id):
        self.name = name
        self.currency_id = currency_id

    def __repr__(self):
        return f'<Bank "{self.name}">'

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "currency": self.currency.json(),
            "author": self.author.json(),
            "creation_date": self.creation_date,
            "update_date": self.update_date
        }
