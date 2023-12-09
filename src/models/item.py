from datetime import datetime

from sqlalchemy.types import UUID

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
    author_id = db.Column(UUID(as_uuid=True),
                          db.ForeignKey('user.id'),
                          nullable=False
                          )
    author = db.relationship('User', backref=db.backref('items', lazy=True))

    def __init__(self, name, author_id, description=None, brand=None, image=None):
        self.name = name
        self.description = description
        self.brand = brand
        self.author_id = author_id
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
            "author": {
                "id": self.author_id,
                "email": self.author.email,
                "username": self.author.username
            }
        }

    def __repr__(self):
        return f'<Item "{self.name}">'
