from src.extensions import db


class Warehouse(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    location = db.Column(db.string())

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __repr__(self):
        return f'<Location "{self.name}">'

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }
