from datetime import datetime, UTC
from src.extensions import db


class Warehouse(db.Model):
    __tablename__ = "warehouse"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    location_id = db.Column(db.Integer(), db.ForeignKey('location.id'))
    creation_date = db.Column(db.DateTime(), default=datetime.now(UTC))
    update_date = db.Column(
        db.DateTime(),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC)
    )

    # Relationships
    location = db.relationship('Location', lazy=True)

    def __init__(
            self,
            name,
            location_id,
            creation_date=None,
            update_date=None
            ):
        self.name = name
        self.location_id = location_id
        if creation_date is not None:
            self.creation_date = creation_date
        if update_date is not None:
            self.update_date = update_date

    def __repr__(self):
        return f'<Location "{self.name}">'

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location.json(),
            "creation_date": self.creation_date,
            "update_date": self.update_date,
        }
