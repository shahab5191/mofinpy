from datetime import datetime
from src.extensions import db


class Transfer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    origin_warehouse_id = db.Column(
        db.Integer(),
        db.ForeignKey('warehouse.id')
    )
    dest_warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id'))
    transfer_price_id = db.Column(db.Integer(), db.ForeignKey('price.id'))
    transfer_date = db.Column(db.DateTime(), default=datetime.utcnow)
    recieved_date = db.Column(db.DateTime())
    price_id = db.Column(db.Integer(), db.ForeignKey('price.id'))

    # Relationships
    origin = db.relationship('Warehouse')
    destination = db.relationship('Warehouse')
    price = db.relationship('Price')

    def __init__(
        self,
        origin_warehouse_id,
        dest_warehouse_id,
        transfer_price_id
    ):
        self.origin_warehouse_id = origin_warehouse_id
        self.dest_warehouse_id = dest_warehouse_id
        self.transfer_price_id = transfer_price_id

    def __repr__(self):
        return f'<Transfer "{self.id}">'

    def json(self):
        return {
            "id": self.id,
            "origin": self.origin.json(),
            "destination": self.destination.json(),
            "transfer date": self.transfer_date,
            "recieved date": self.recieved_date,
            "price": self.price.json()
        }
