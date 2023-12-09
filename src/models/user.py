from datetime import datetime
from sqlalchemy.types import UUID
from src.extensions import db
import uuid


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(40))
    username = db.Column(db.String(40))
    password = db.Column(db.String())
    salt = db.Column(db.String())
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def json(self):
        return {"email": self.email, "id": self.id}

    def __repr__(self):
        return f'<User "{self.email}">'
