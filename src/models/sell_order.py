from datetime import datetime, UTC
from src.extensions import db


class SellOrder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inventory_id = db.Column(db.Integer(), db.ForeignKey('inventory.id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    payment = db.Column(db.Float())
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    creation_date = db.Column(db.DateTime(), default=datetime.now(UTC))
    update_date = db.Column(
        db.DateTime(),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC)
    )
    state = db.Column(db.Enum(
                      'Ordered',
                      'Shipped',
                      'Recieved',
                      'Canceled',
                      name='sell_states'))

    # Relationships
    inventory = db.relationship('Inventory')
    customer = db.relationship('Customer')
    currency = db.relationship('Currency')

    def __init__(
            self,
            inventory_id,
            customer_id,
            payment,
            currency_id,
            state=None,
            creation_date=None,
            update_date=None
            ):
        self.inventory_id = inventory_id
        self.customer_id = customer_id
        self.payment = payment
        self.currency_id = currency_id
        if state is not None:
            self.state = state
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def __repr__(self):
        return f'<SellOrder "{self.id}">'

    def json(self):
        return {
            "id": self.id,
            "inventory": self.inventory.json(),
            "customer": self.customer.json(),
            "payment": self.payment,
            "currency_id": self.currency.json(),
            "creation_date": self.creation_date,
            "update_date": self.update_date
        }
