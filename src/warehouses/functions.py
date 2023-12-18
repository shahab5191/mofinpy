from sqlalchemy import func
from src.models.warehouse import Warehouse
from src.extensions import db


def list_warehouses(offset, limit):
    count = db.session.query(func.count(
                             Warehouse.id)).scalar()
    warehouses = Warehouse.query.order_by(
        Warehouse.update_date).limit(limit).offset(offset).all()

    return {"count": count, "arr": warehouses}


def create_warehouse(author_id, **kwargs):
    name = kwargs['name']
    location_id = kwargs['location_id']
    creation_date = kwargs.get('creation_date', None)
    update_date = kwargs.get('update_date', None)
    new_warehouse = Warehouse(
        name=name,
        location_id=location_id,
        author_id=author_id,
        creation_date=creation_date,
        update_date=update_date
    )

    db.session.add(new_warehouse)
    db.session.commit()

    return new_warehouse.json()


def update_warehouse(id, **kwargs):
    warehouse = Warehouse.query.get(id)
    if warehouse is None:
        raise Exception(f'Warehouse with id:{id} was not found!')

    warehouse.name = kwargs.get('name', warehouse.name)
    warehouse.location_id = kwargs.get('location_id', warehouse.location_id)
    warehouse.creation_date = kwargs.get(
        'creation_date', warehouse.creation_date)
    warehouse.update_date = kwargs.get('update_date', warehouse.update_date)

    db.session.commit()

    return warehouse.json()


def delete_warehouse(id):
    warehouse = Warehouse.query.get(id)
    if warehouse is None:
        raise Exception(f'Warehouse with id:{id} was not found!')

    db.session.delete(warehouse)
    db.session.commit()
    return
