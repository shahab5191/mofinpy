from datetime import datetime
from src.extensions import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image = db.Column(db.String())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    description = db.Column(db.Text())
    brand = db.Column(db.String())

    def __init__(self, name, description=None, brand=None, image=None):
        self.name = name
        self.description = description
        self.brand = brand
        self.image = image

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "createion_date": self.creation_date,
            "update_date": self.update_date,
            "description": self.description,
            "brand": self.brand,
            "image": self.image,
        }

    def __repr__(self):
        return f'<Item "{self.name}">'
