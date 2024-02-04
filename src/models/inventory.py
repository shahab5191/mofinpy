from datetime import datetime, UTC
from src.extensions import db


class Inventory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(
        db.Integer(),
        db.ForeignKey('item.id'),
        nullable=False
    )
    quantity = db.Column(db.Integer())
    creation_date = db.Column(db.DateTime, default=datetime.now(UTC))
    update_date = db.Column(
        db.DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC)
    )
    price = db.Column(db.Float())
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    base_currency_rate = db.Column(db.Float())
    warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id'))
    purchase_id = db.Column(
        db.Integer(),
        db.ForeignKey('purchase_order.id', ondelete='CASCADE'))
    provider_id = db.Column(db.Integer(), db.ForeignKey('provider.id'))

    # Relationships
    item = db.relationship('Item', lazy=True)
    currency = db.relationship('Currency', lazy=True)
    warehouse = db.relationship('Warehouse', lazy=True)
    purchase = db.relationship(
        'PurchaseOrder', lazy=True,
        cascade="all, delete"
    )
    provider = db.relationship('Provider', lazy=True)

    def __init__(
        self,
        item_id,
        quantity,
        price,
        currency_id,
        base_currency_rate,
        purchase_id,
        provider_id,
        warehouse_id=None,
        creation_date=None,
        update_date=None,
    ):
        self.item_id = item_id
        self.quantity = quantity
        self.price = price
        self.currency_id = currency_id
        self.base_currency_rate = base_currency_rate
        self.purchase_id = purchase_id
        self.provider_id = provider_id
        if warehouse_id is not None:
            self.warehouse_id = warehouse_id
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def json(self):
        return {
            "id": self.id,
            "item": self.item.json(),
            "quantity": self.quantity,
            "creation_date": self.creation_date,
            "update_date": self.update_date,
            "warehouse": self.warehouse.json(),
            "price": self.price,
            "currency": self.currency.json(),
            "base_currency_rate": self.base_currency_rate,
            "purchase_order": self.purchase.json(),
            "provider": self.provider.json()
        }

    def __repr__(self) -> str:
        return f'<Inventory "{self.item.name}">'
