from datetime import datetime
from src.extensions import db


class PurchaseOrder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    to_rial_rate = db.Column(db.Float(), nullable=False)
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    quantity = db.Column(db.Integer(), nullable=False)
    provider_id = db.Column(db.Integer(), db.ForeignKey(
        'provider.id'), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id'))
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    state = db.Column(db.Enum("Ordered", "Shipped",
                      "Canceled", "Received", name='purchase_states'))
    make_unique = db.Column(db.Boolean(), default=False)

    # RelationShips
    provider = db.relationship('Provider', lazy=True)
    item = db.relationship('Item', lazy=True)
    warehouse = db.relationship('Warehouse', lazy=True)
    currency = db.relationship('Currency', lazy=True)

    def __init__(
            self,
            quantity,
            provider_id,
            make_unique,
            item_id,
            price,
            to_rial_rate,
            currency_id,
            warehouse_id=None,
            creation_date=None,
            update_date=None,
            state="Ordered"
    ):
        self.quantity = quantity
        self.provider_id = provider_id
        self.state = state
        self.make_unique = make_unique
        self.price = price
        self.item_id = item_id
        self.to_rial_rate = to_rial_rate
        self.currency_id = currency_id
        if warehouse_id is not None:
            self.warehouse_id = warehouse_id
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def json(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "provider": self.provider.json(),
            "creation_date": self.creation_date,
            "update_date": self.update_date,
            "state": self.state,
            "make_unique": self.make_unique,
            "price": self.price,
            "item": self.item.json(),
            "to_rial_rate": self.to_rial_rate,
            "currency": self.currency.json(),
            "warehouse": self.warehouse.json() if self.warehouse is not None else None,
        }

    def __repr__(self) -> str:
        return f'<Order "{self.id}">'
