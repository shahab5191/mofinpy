from src.extensions import db


class TREnums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<TREnum "{self.name}">'

    def json(self):
        return self.name
