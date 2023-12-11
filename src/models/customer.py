from src.extensions import db


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    address = db.column(db.String())

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self) -> str:
        return f'<Customer "{self.name}">'

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }
