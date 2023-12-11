from sqlalchemy import func
from src.extensions import db
from src.models.inventory import Inventory


def get_inventory_list(offset, limit):
    count = db.session.query(func.count(Inventory.id)).scalar()
    inventory = Inventory.query.order_by(
        Inventory.creation_date).offset(offset).limit(limit).all()
    return {"count": count, "inventory": inventory}
