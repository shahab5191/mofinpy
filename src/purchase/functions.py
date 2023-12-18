from src.extensions import db
from src.models.inventory import Inventory
from src.models.purchase_order import PurchaseOrder
from src.purchase.schemas import PurchaseOrderStates


def purchase_to_invetories(make_unique, quantity, **data):
    try:
        if make_unique is True:
            for _ in range(quantity):
                create_inventory(1, **data)

        else:
            create_inventory(quantity, **data)
    except Exception as err:
        print('[purchase_to_inventory]', err)
        raise err


def create_inventory(quantity, **data):
    new_inventory = Inventory(quantity=quantity, **data)
    db.session.add(new_inventory)
    db.session.commit()
    return new_inventory


def create_purchase(author_id,
                    item_id,
                    price,
                    currency_id,
                    to_rial_rate,
                    make_unique,
                    provider_id,
                    quantity=1,
                    warehouse_id=None,
                    state='Ordered',
                    creation_date=None,
                    update_date=None
                    ):
    try:
        new_purchase = PurchaseOrder(
            quantity=quantity,
            provider_id=provider_id,
            author_id=author_id,
            creation_date=creation_date,
            state=state,
            update_date=update_date,
            make_unique=make_unique,
            price=price,
            to_rial_rate=to_rial_rate,
            item_id=item_id,
            warehouse_id=warehouse_id,
            currency_id=currency_id
        )

        if creation_date is not None:
            new_purchase.creation_date = creation_date
        if update_date is not None:
            new_purchase.update_date = update_date

        db.session.add(new_purchase)
        db.session.commit()
    except Exception as err:
        print('[create_purchase]', err)
        return {"err": "Somthing went wrong! please try again later"}, 500

    try:
        purchase_to_invetories(
            item_id=item_id,
            author_id=author_id,
            price=price,
            currency_id=currency_id,
            to_rial_rate=to_rial_rate,
            purchase_id=new_purchase.id,
            quantity=quantity,
            make_unique=make_unique,
            provider_id=provider_id,
            warehouse_id=warehouse_id,
            creation_date=creation_date,
            update_date=update_date
        )
    except Exception as err:
        db.session.rollback()
        db.session.delete(new_purchase)
        db.session.commit()
        print('[create_purchase]', err)
        return {"err": "Something went wrong!, please try again later"}, 500

    return {"Purchase Order": new_purchase.json()}, 201


def update_purchase(id, **data):
    purchase = PurchaseOrder.query.get(id)

    if purchase is None:
        return {"err": f'Purchase Order number {id} does not exist!'}, 404

    if purchase.state == PurchaseOrderStates.Received.value:
        return {"err": f'Purchase Order number {
            id} is Recieved and cannot be changed!'}, 400

    inventories = Inventory.query.where(Inventory.purchase_id == id).all()
    if len(inventories) != 0:
        print(inventories)
        return {"err": "This action could not be completed! please contact admin"}, 500

    item_id = data.get('item_id', purchase.item_id)
    author_id = data.get('author_id', purchase.author_id)
    price = data.get('price', purchase.price)
    currency_id = data.get('currency_id', purchase.currency_id)
    to_rial_rate = data.get('to_rial_rate', purchase.to_rial_rate)
    creation_date = data.get('creation_date', purchase.creation_date)
    update_date = data.get('update_date', None)
    quantity = data.get('quantity', purchase.quantity)
    provider_id = data.get('provider_id', purchase.provider_id)
    make_unique = data.get('make_unique', purchase.make_unique)
    warehouse_id = data.get('warehouse_id', purchase.warehouse_id)

    try:
        purchase_to_invetories(
            item_id=item_id,
            author_id=author_id,
            price=price,
            currency_id=currency_id,
            to_rial_rate=to_rial_rate,
            purchase_id=purchase.id,
            quantity=quantity,
            make_unique=make_unique,
            provider_id=provider_id,
            warehouse_id=warehouse_id,
            creation_date=creation_date,
            update_date=update_date
        )
    except Exception as err:
        print(['update_purchase'], err)
        return {"err": "Somthing went wrong! please try again later"}

    purchase.state = 'Received'
    purchase.item_id = item_id
    purchase.price = price
    purchase.currency_id = currency_id
    purchase.to_rial_rate = to_rial_rate
    purchase.creation_date = creation_date
    purchase.update_date = update_date
    purchase.quantity = quantity
    purchase.provider_id = provider_id
    purchase.make_unique = make_unique
    purchase.warehouse_id = warehouse_id
    db.session.commit()
    return purchase.json()


def delete_purchase(id):
    purchase = PurchaseOrder.query.get(id)
    if purchase is None:
        return ({"err": f'Item number {id} was not found!'}, 404)
    if purchase.state == PurchaseOrderStates.Received.value:
        return (
            {"err": f'Item number {id} is "Completed" and cannot be deleted!'},
            400)
    db.session.delete(purchase)
    db.session.commit()
    return {"msg": f'Item number {id} deleted successfully!'}, 201
