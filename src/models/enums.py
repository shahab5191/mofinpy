from src.extensions import db


class Enum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String())
    value = db.Column(db.String())

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<TREnum "{self.model}: {self.value}">'

    def json(self):
        return {
            "model": self.model,
            "value": self.value
        }
