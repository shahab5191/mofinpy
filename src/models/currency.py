from src.extensions import db


class Currency(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    unit = db.Column(db.String(20))

    def __init__(self, unit):
        self.unit = unit

    def __repr__(self):
        return f'<Currency "{self.unit}">'

    def json(self):
        return {
            "id": self.id,
            "unit": self.unit
        }
