from datetime import datetime
from sqlalchemy import event
from src.extensions import db


class Transactions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    amount = db.Column(db.Float())

    # Relationships
    currency = db.relationship('Currency')

    def __init__(self,
                 currency_id,
                 amount,
                 creation_date=None,
                 update_date=None,
                 ):
        self.currency_id = currency_id
        self.amount = amount
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def __repr__(self):
        return f'<Transaction "{self.amount}">'

    def json(self):
        return {
            "id": self.id,
            "currency": self.currency.json(),
            "amount": self.amount,
            "creation_date": self.creation_date,
            "update_date": self.update_date
        }

# TODO: implement bank update functionality


def update_bank(mapper, conncetion, target):
    print(target)


event.listen(Transactions, 'after_insert', update_bank)
