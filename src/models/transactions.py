from datetime import datetime, UTC
from sqlalchemy import event
from sqlalchemy.orm import Session
from src.extensions import db
from src.models.bank import Bank


class Transactions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    creation_date = db.Column(db.DateTime(), default=datetime.now(UTC))
    update_date = db.Column(
        db.DateTime(),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC)
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


@event.listens_for(Transactions, 'after_insert')
def update_bank(mapper, connection, target):
    db_engine = connection.engine
    session = Session(bind=db_engine)

    currency = target.currency_id
    amount = target.amount
    bank = session.query(Bank).where(
        Bank.currency_id == currency
    ).with_for_update().first()
    if bank is None:
        print(['update_bank'], f'Bank with currency: {
              currency} does not exist!')
        raise Exception('Bank with this currency does not exist!')
    bank.balance += amount

    session.commit()
