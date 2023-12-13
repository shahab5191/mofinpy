from datetime import datetime
from src.extensions import db


class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    amount_id = db.Column(db.Integer(), db.ForeignKey('price.id'))
    description = db.Column(db.Text())
    reason_id = db.Column(db.Integer(), db.ForeignKey('enum.id'))
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    bank_id = db.Column(db.Integer(), db.ForeignKey('bank.id'))

    # Relationships
    reason = db.relationship('Enum')
    author = db.relationship('User')
    amount = db.relationship('Price')
    bank = db.relationship('Bank')

    def __init__(
            self,
            amount_id,
            description,
            reason_id,
            author_id,
            bank_id
            ):
        self.amount_id = amount_id
        self.description = description
        self.reason_id = reason_id
        self.author_id = author_id
        self.bank_id = bank_id

    def __repr__(self) -> str:
        return f'<Transaction "{self.amount.price}">'

    def json(self):
        return {
            "id": self.id,
            "amount": self.amount.json(),
            "bank": self.json(),
            "description": self.description,
            "reason": self.reason.json(),
            "author": self.author.json(),
            "creation_date": self.creation_date,
            "update_date": self.update_date,
        }
