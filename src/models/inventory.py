from datetime import datetime
from src.extensions import db


class Inventory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(
        db.Integer(),
        db.ForeignKey('item.id'),
        nullable=False
    )
    author_id = db.Column(
        db.UUID(),
        db.ForeignKey('user.id'),
        nullable=False
    )
    quantity = db.Column(db.Integer())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    price_id = db.Column(db.Integer(), db.ForeignKey('price.id'))
    warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id'))

    # Relationships
    item = db.relationship('Item')
    author = db.relationship(
        'User',
        backref=db.backref('inventory_item', lazy=True)
    )
    price = db.relationship('Price', lazy=True)
    warehouse = db.relationship('Warehouse')

    def __init__(
        self,
        item_id,
        author_id,
        quantity,
        price_id,
        warehouse_id
    ):
        self.item_id = item_id
        self.author_id = author_id
        self.quantity = quantity
        self.price_id = price_id
        self.warehouse_id = warehouse_id

    def json(self):
        return {
            "id": self.id,
            "item": self.item.json(),
            "author": self.author.json(),
            "quantity": self.quantity,
            "creation_date": self.creation_date,
            "update_date": self.update_date,
            "warehouse": self.warehouse.json(),
            "price": self.price.json()
        }

    def __repr__(self) -> str:
        return f'<Inventory "{self.item.name}">'
