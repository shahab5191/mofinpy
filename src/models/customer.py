from datetime import datetime
from src.extensions import db


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(40))
    tel = db.Column(db.String(40))
    contact_person = db.Column(db.String(40))
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    location_id = db.Column(db.Integer(), db.ForeignKey('location.id'))
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    currency = db.relationship('Currency')
    location = db.relationship('Location')

    def __init__(
            self,
            name,
            email,
            tel,
            contact_person,
            currency_id,
            location_id,
            creation_date=None,
            update_date=None
            ):
        self.name = name
        self.email = email
        self.tel = tel
        self.contact_person = contact_person
        self.currency_id = currency_id
        self.location_id = location_id
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def __repr__(self) -> str:
        return f'<Customer "{self.name}">'

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "tel": self.tel,
            "contact_person": self.contact_person,
            "currency": self.currency.json(),
            "location": self.location.json(),
            "creation_date": self.creation_date,
            "update_date": self.update_date,
        }
