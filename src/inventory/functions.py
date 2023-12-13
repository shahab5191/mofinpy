from sqlalchemy import func
from src.extensions import db
from src.models.inventory import Inventory


def get_inventory_list(offset, limit):
    count = db.session.query(func.count(Inventory.id)).scalar()
    inventory = Inventory.query.order_by(
        Inventory.creation_date).offset(offset).limit(limit).all()
    return {"count": count, "inventory": inventory}


def create_inventory(
        item_id,
        author_id,
        price,
        currency_id,
        to_rial_rate,
        purchase_id,
        quantity=1,
        creation_date=None,
        update_date=None
        ):
    new_inventory = Inventory(
        item_id=item_id,
        author_id=author_id,
        price=price,
        currency_id=currency_id,
        to_rial_rate=to_rial_rate,
        purchase_id=purchase_id,
        quantity=quantity
    )

    if creation_date is not None:
        new_inventory.creation_date = creation_date
    if update_date is not None:
        new_inventory.update_date = update_date

    db.session.add(new_inventory)
    db.session.commit()

    return new_inventory
