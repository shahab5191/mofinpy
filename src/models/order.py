from datetime import datetime
from src.extensions import db


class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer())
    provider = db.Column(db.String())
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'))
    warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id'))
    price_id = db.Column(db.Integer(), db.ForeignKey('price.id'))
    order_date = db.Column(db.DateTime())
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # RelationShips
    item = db.relationship('Item')
    warehouse = db.relationship('Warehouse')
    price = db.relationship("Price")

    def __init__(self, quantity, provider, item_id, warehouse_id, price_id):
        self.quantity = quantity
        self.provider = provider
        self.item_id = item_id
        self.price_id = price_id
        self.warehouse_id = warehouse_id

    def json(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "provider": self.provider,
            "item": self.item.json(),
            "warehouse": self.warehouse.json(),
            "price": self.price.json(),
            "order_date": self.order_date,
        }

    def __repr__(self) -> str:
        return f'<Order "{self.id}">'
