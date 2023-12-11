from datetime import datetime
from src.extensions import db


class Delivery(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sales_date = db.Column(db.DateTime(), default=datetime.utcnow)
    quantity = db.Column(db.Integer())
    delivery_date = db.Column(db.Integer())
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    inventory_id = db.Column(db.Integer(), db.ForeignKey('inventory.id'))
    warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # Relationships
    customer = db.relationship('Customer')
    inventory = db.relationship('Inventory')
    warehouse = db.relationship('Warehouse')
    author = db.relationship('User')

    def __init__(
            self,
            quantity,
            customer_id,
            inventory_id,
            warehouse_id,
            author_id,
            delivery_date=None,
            sales_date=None,
            ):
        self.quantity = quantity
        self.customer_id = customer_id
        self.warehouse_id = warehouse_id
        self.inventory_id = inventory_id
        self.author_id = author_id
        if delivery_date is not None:
            self.delivery_date = delivery_date
        if sales_date is not None:
            self.sales_date = sales_date

    def __repr__(self):
        return f'<Delivery "{self.id}">'

    def json(self):
        return {
            "id": self.id,
            "sales date": self.sales_date,
            "quantity": self.quantity,
            "delivery date": self.delivery_date,
            "customer": self.customer.json(),
            "warehouse": self.warehouse.json(),
            "inventory": self.inventory.json(),
            "author": self.author.json()
        }
