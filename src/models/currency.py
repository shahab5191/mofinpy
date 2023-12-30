from datetime import datetime, UTC
from sqlalchemy.orm import Session

from sqlalchemy.sql.base import event
from src.extensions import db
from src.models.bank import Bank


class Currency(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    unit = db.Column(db.String(20))
    creation_date = db.Column(db.DateTime(), default=datetime.now(UTC))
    update_date = db.Column(db.DateTime(),
                            default=datetime.now(UTC),
                            onupdate=datetime.now(UTC)
                            )

    def __init__(self, unit):
        self.unit = unit

    def __repr__(self):
        return f'<Currency "{self.unit}">'

    def json(self):
        return {
            "id": self.id,
            "unit": self.unit,
            "creation_date": self.creation_date,
            "update_date": self.update_date
        }


@event.listens_for(Currency, 'after_insert')
def create_bank(mapper, connection, target):
    currency_id = target.id
    name = target.unit

    db_engine = connection.engine
    session = Session(bind=db_engine)

    new_bank = Bank(name=name, currency_id=currency_id)
    session.add(new_bank)
    session.commit()
