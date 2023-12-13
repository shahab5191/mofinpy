from sqlalchemy import func
from src.extensions import db
from src.models.item import Item


def get_items(offset, limit):
    count = db.session.query(func.count(Item.id)).scalar()
    items = Item.query.order_by(Item.creation_date).offset(offset).limit(limit).all()
    return {"count": count, "arr": items}


def create_item(name, author_id, image=None, description=None, brand=None):
    new_item = Item(name=name, author_id=author_id)
    if image:
        new_item.image = image
    if description:
        new_item.description = description
    if brand:
        new_item.brand = brand
    db.session.add(new_item)
    db.session.commit()
    return new_item


def get_item_by_id(item_id):
    try:
        found_item = Item.query.get(item_id)
    except Exception as err:
        print(err)
        return None

    return found_item


def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        raise Exception('Item was not found!')
    db.session.delete(item)
    db.session.commit()
    return


def update_item(item_id, **kwargs):
    item = Item.query.get(item_id)
    if item is None:
        raise Exception('Item was not found!')

    if 'name' in kwargs:
        item.name = kwargs['name']
    if 'image' in kwargs:
        item.image = kwargs['image']
    if 'description' in kwargs:
        item.description = kwargs['description']
    if 'brand' in kwargs:
        item.brand = kwargs['brand']
    db.session.commit()


def search_items(query, offset, limit):
    results = Item.query.filter(Item.name.ilike(f"%{query}%")).offset(offset).limit(limit).all()
    res_json = [item.json() for item in results]
    return res_json
