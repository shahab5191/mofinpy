from datetime import datetime, UTC
from src.extensions import db


class Location(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(40))
    city = db.Column(db.String(40))
    address = db.Column(db.Text())
    creation_date = db.Column(db.DateTime(), default=datetime.now(UTC))
    update_date = db.Column(
        db.DateTime(),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC)
    )

    def __init__(
            self,
            address,
            country=None,
            city=None,
            creation_date=None,
            update_date=None,
            ):

        self.address = address
        if country is not None:
            self.country = country
        if city is not None:
            self.city = city
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def __repr__(self):
        return f'Location "{self.country}/{self.city}"'

    def json(self):
        return {
            "id": self.id,
            "country": self.country,
            "city": self.city,
            "address": self.address,
            "creation_date": self.creation_date,
            "update_date": self.update_date
        }
