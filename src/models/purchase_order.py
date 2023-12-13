from datetime import datetime
from src.extensions import db


class PurchaseOrder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer())
    provider_id = db.Column(db.Integer(), db.ForeignKey('provider.id'))
    order_date = db.Column(db.DateTime(), default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    author_id = db.Column(
        db.UUID(),
        db.ForeignKey('user.id')
    )
    state = db.Column(db.Enum("pending", "completed",
                      "canceled", name='invnetory_states'))

    # RelationShips
    provider = db.relationship('Provider', lazy=True)
    author = db.relationship('User', lazy=True)

    def __init__(
            self,
            quantity,
            provider_id,
            author_id,
            order_date=None,
            update_date=None,
            state="pending"
    ):
        self.quantity = quantity
        self.provider_id = provider_id
        self.author_id = author_id
        self.state = state
        if order_date is not None:
            self.order_date = order_date
        if update_date is not None:
            self.update_date = update_date

    def json(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "provider": self.provider.json(),
            "order_date": self.order_date,
            "update_date": self.update_date,
            "author": self.author.json(),
            "state": self.state
        }

    def __repr__(self) -> str:
        return f'<Order "{self.id}">'
