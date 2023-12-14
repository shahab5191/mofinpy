from sqlalchemy import func
from src.extensions import db
from src.inventory.functions import create_inventory
from src.models.inventory import Inventory
from src.models.purchase_order import PurchaseOrder


def get_purchases(offset, limit):
    count = db.session.query(func.count(PurchaseOrder.id)).scalar()
    purchases = PurchaseOrder.query.order_by(
        PurchaseOrder.update_date).offset(offset).limit(limit).all()
    return {"count": count, "arr": purchases}


def create_purchase(author_id, **kwargs):
    item_id = kwargs['item_id']
    price = kwargs['price']
    currency_id = kwargs['currency_id']
    to_rial_rate = kwargs['to_rial_rate']
    quantity = int(kwargs['quantity'])
    creation_date = kwargs['order_date'] if 'order_date' in kwargs else None
    update_date = kwargs['update_date'] if 'update_date' in kwargs else None
    make_unique = bool(kwargs['make_unique'])
    provider_id = kwargs['provider_id']
    new_purchase = PurchaseOrder(
        quantity=quantity,
        provider_id=provider_id,
        author_id=author_id,
        order_date=creation_date
    )

    if creation_date is not None:
        new_purchase.order_date = creation_date
    if update_date is not None:
        new_purchase.update_date = update_date

    db.session.add(new_purchase)
    db.session.commit()

    try:
        if make_unique is True:
            for _ in range(quantity):
                create_inventory(
                    item_id=item_id,
                    author_id=author_id,
                    price=price,
                    currency_id=currency_id,
                    to_rial_rate=to_rial_rate,
                    purchase_id=new_purchase.id,
                    creation_date=creation_date,
                    update_date=update_date
                )

        else:
            create_inventory(
                item_id=item_id,
                author_id=author_id,
                price=price,
                currency_id=currency_id,
                to_rial_rate=to_rial_rate,
                purchase_id=new_purchase.id,
                creation_date=creation_date,
                update_date=update_date,
                quantity=quantity
            )
    except Exception as err:
        db.session.rollback()
        db.session.delete(new_purchase)
        db.session.commit()
        raise Exception(err)

    return new_purchase


def update_purchase(id, **kwargs):
    purchase = PurchaseOrder.query.get(id)

    if purchase is None:
        raise Exception(f'Purchase Order number {id} does not exist!')

    inventories = Inventory.query.where(Inventory.purchase_id == id).all()

    for inventory in inventories:
        if 'item_id' in kwargs:
            inventory.item_id = kwargs['item_id']
        if 'price' in kwargs:
            inventory.price = kwargs['price']
        if 'currency_id' in kwargs:
            inventory.currency_id = kwargs['currency_id']
        if 'to_rial_rate' in kwargs:
            inventory.to_rial_rate = kwargs['to_rial_rate']
        if 'provider_id' in kwargs:
            inventory.provider_id = kwargs['provider_id']
        if 'order_date' in kwargs:
            inventory.creation_date = kwargs['order_date']
        if 'update_date' in kwargs:
            inventory.update_date = kwargs['update_date']

    if 'order_date' in kwargs:
        purchase.order_date = kwargs['order_date']
    if 'update_date' in kwargs:
        purchase.update_date = kwargs['update_date']

    db.session.commit()

    return purchase.json()


def delete_purchase(id):
    purchase = PurchaseOrder.query.get(id)
    if purchase is None:
        raise Exception(f'Item number {id} was not found!')
    if purchase.state == "completed":
        raise Exception(f'Item number {id} is Completed and cannot be deleted!')
    db.session.delete(purchase)
    db.session.commit()
    return