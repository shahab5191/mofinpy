from src.extensions import db


class Location(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(40))
    city = db.Column(db.String(40))
    address = db.Column(db.Text())

    def __init__(self, country, city, address):
        self.country = country
        self.city = city
        self.address = address

    def __repr__(self):
        return f'Location "{self.country}/{self.city}"'

    def json(self):
        return {
            "id": self.id,
            "country": self.country,
            "city": self.city,
            "address": self.address
        }
