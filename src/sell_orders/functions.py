from sqlalchemy import func
from src.extensions import db
from src.models.sell_order import SellOrder


def list_sell_orders(limit, offset):
    count = db.session.query(func.count(
                             SellOrder.id)).scalar()
    sell_orders = SellOrder.query.order_by(
        SellOrder.update_date).limit(limit).offset(offset).all()
    return {"count": count, "arr": sell_orders}


def create_sell_order(author_id, **kwargs):
    inventory_id = kwargs['inventory_id']
    customer_id = kwargs['customer_id']
    payment = kwargs['payment']
    currency_id = kwargs['currency_id']
    author_id = kwargs['author_id']
    creation_date = kwargs.get('creation_date', None)
    update_date = kwargs.get('update_date', None)
    state = kwargs.get('state', None)

    new_sell_order = SellOrder(
        inventory_id=inventory_id,
        customer_id=customer_id,
        payment=payment,
        currency_id=currency_id,
        author_id=author_id,
        creation_date=creation_date,
        update_date=update_date,
        state=state
    )

    db.session.add(new_sell_order)
    db.session.commit()

    return new_sell_order.json()


def update_sell_order(id, **kwargs):
    sell_order = SellOrder.query.get(id)
    if sell_order is None:
        raise Exception(f'Sell Order id:{id} was not found!')

    sell_order.inventory_id = kwargs.get(
        'inventory_id', sell_order.inventory_id)
    sell_order.customer_id = kwargs.get('customer_id', sell_order.customer_id)
    sell_order.payment = kwargs.get('payment', sell_order.payment)
    sell_order.currency_id = kwargs.get('currency_id', sell_order.currency_id)
    sell_order.state = kwargs.get('state', sell_order.state)
    sell_order.creation_date = kwargs.get(
        'creation_date', sell_order.creation_date)
    sell_order.update_date = kwargs.get('update_date', sell_order.update_date)

    db.session.commit()

    return {"sell_order": sell_order}


def delete_sell_order(id):
    sell_order = SellOrder.query.get(id)
    if sell_order is None:
        raise Exception(f'Sell Order id:{id} was not found!')

    db.session.delete(sell_order)
    db.session.commit()

    return
