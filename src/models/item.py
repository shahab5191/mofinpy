from datetime import datetime
from src.extensions import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image_id = db.Column(db.Integer(), db.ForeignKey('image_meta.id'))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    description = db.Column(db.Text())
    brand = db.Column(db.String())

    # Relationships
    image = db.relationship('ImageMeta')

    def __init__(self, name, description=None, brand=None, image_id=None):
        self.name = name
        self.description = description
        self.brand = brand
        self.image_id = image_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "createion_date": self.creation_date,
            "update_date": self.update_date,
            "description": self.description,
            "brand": self.brand,
            "image": self.image.json(),
        }

    def __repr__(self):
        return f'<Item "{self.name}">'
