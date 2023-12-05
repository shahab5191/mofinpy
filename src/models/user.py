from datetime import datetime
from sqlalchemy.types import UUID
from src.extensions import db
import uuid


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(40))
    password = db.Column(db.String(24))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        default_factory=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f'<Post "{self.email}">'
