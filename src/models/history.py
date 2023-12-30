from datetime import datetime, UTC
from src.extensions import db


class History(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    creation_date = db.Column(db.DateTime(), default=datetime.now(UTC))
    user_id = db.Column(db.UUID(), db.ForeignKey('user.id'), nullable=False)
    model_name = db.Column(db.String(), nullable=False)
    record_id = db.Column(db.Integer(), nullable=False)
    action = db.Column(db.String(), nullable=False)
    changes = db.Column(db.String())

    # Relationships
    user = db.relationship('User', lazy=True)

    def __init__(self,
                 user_id,
                 model_name,
                 record_id,
                 action,
                 changes=None
                 ):
        self.user_id = user_id
        self.model_name = model_name
        self.record_id = record_id
        self.action = action,
        self.changes = changes

    def __repr__(self):
        return f'<History "{self.model_name}">'

    def json(self):
        return {
            "user": self.user.json(),
            "model_name": self.model_name,
            "record_id": self.record_id,
            "action": self.action,
            "changes": self.changes
        }
