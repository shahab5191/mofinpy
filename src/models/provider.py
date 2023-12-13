from datetime import datetime
from src.extensions import db


class Provider(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40))
    website = db.Column(db.String())
    email = db.Column(db.String(50))
    tel = db.Column(db.String(20))
    contact_person = db.Column(db.String(40))
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'))
    location_id = db.Column(db.Integer(), db.ForeignKey('location.id'))
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    location = db.relationship('Location')
    currency = db.relationship('Currency')

    def __init__(
            self,
            name,
            email,
            tel,
            contact_person,
            currency_id,
            location_id,
            website=None,
            creation_date=None,
            update_date=None
            ):
        self.name = name
        self.email = email
        self.tel = tel
        self.contact_person = contact_person
        self.currency_id = currency_id
        self.location_id = location_id
        if website is not None:
            self.website = website
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def __repr__(self):
        return f'Provider "{self.name}"'

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "tel": self.tel,
            "contact_person": self.contact_person,
            "currency": self.currency.json(),
            "location": self.location.json()
        }
