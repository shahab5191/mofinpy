from src.extensions import db


class Price(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.Float())
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    base_currency_rate = db.Column(db.Float())

    # Relationships
    currency = db.relationship('Currency')

    def __init__(self, price, currency_id, base_currency_rate):
        self.price = price
        self.currency_id = currency_id
        self.base_currency_rate = base_currency_rate

    def __repr__(self):
        return f'<Price "{self.price} {self.currency.name}">'

    def json(self):
        return {
            "id": self.id,
            "price": self.price,
            "currency": self.currency.json(),
            "base_currency_rate": self.base_currency_rate
        }
