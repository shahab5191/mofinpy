from src.extensions import db


class Price(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.Float())
    price_rial = db.Column(db.Float())
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    to_rial_ratio = db.Column(db.Float())

    # Relationships
    currency = db.relationship('Currency')

    def __init__(self, price, currency_id, to_rial_ratio):
        self.price = price
        self.currency_id = currency_id
        self.to_rial_ratio = to_rial_ratio
        self.price_rial = price * to_rial_ratio

    def __repr__(self):
        return f'<Price "{self.price} {self.currency.name}">'

    def json(self):
        return {
            "id": self.id,
            "price": self.price,
            "price_rial": self.price_rial,
            "currency": self.currency.json(),
            "to_rial_ratio": self.to_rial_ratio
        }
