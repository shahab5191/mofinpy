from src.models.item import Item


def search_items(query, offset, limit):
    results = Item.query.filter(Item.name.ilike(
        f"%{query}%")).offset(offset).limit(limit).all()
    res_json = [item.json() for item in results]
    return res_json
