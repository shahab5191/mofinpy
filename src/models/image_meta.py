from datetime import datetime, UTC

from flask import request
from src.extensions import db


class ImageMeta(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.now(UTC))
    update_date = db.Column(db.DateTime(),
                            default=datetime.now(UTC),
                            onupdate=datetime.now(UTC)
                            )

    def __init__(self, filename) -> None:
        self.filename = filename

    def __repr__(self) -> str:
        return f'<Media "{self.filename}">'

    def json(self):
        return {
            "id": self.id,
            "filename": request.url_root + "uploads/" + self.filename,
            "creation_date": self.creation_date,
        }
