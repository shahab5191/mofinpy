from datetime import datetime
from src.extensions import db


class Bank(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40))
    currency_id = db.Column(db.Integer(),
                            db.ForeignKey('currency.id'),
                            nullable=False
                            )
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    balance = db.Column(db.Float(), default=0, nullable=False)
    update_date = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    currency = db.relationship('Currency')

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
            "creation_date": self.creation_date,
            "update_date": self.update_date
        }
