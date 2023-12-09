from marshmallow import ValidationError
from src.items import bp
from src.items.functions import create_item, delete_item, get_item_by_id, get_items, search_items, update_item
from src.items.schemas import CreateItemSchema, UpdateItemSchema
from src.utils.protect_route import protected_route
from flask import g, jsonify, request


@bp.route('/items/', methods=['GET'])
@protected_route
def items():
    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 20)

    found_items = get_items(offset, limit)
    json_found_items = [item.json() for item in found_items["items"]]
    return {
        "items": json_found_items,
        "len": len(json_found_items),
        "offset": offset,
        "limit": limit,
        "pages": int((found_items["count"] - offset) / limit)
    }


@bp.route('/items/', methods=['POST'])
@protected_route
def items_create():
    json_data = request.json
    if not json_data:
        return {"err": "You should provide data"}, 400

    schema = CreateItemSchema()
    try:
        result = schema.load(json_data)
    except ValidationError as err:
        print(err)
        return {"err": "data are not valid!"}, 400
    if type(result) is not dict:
        return {"err": "err"}
    name = result['name'] if 'name' in result else None
    image = result['image'] if 'image' in result else None
    author_id = g.user_data['id']
    description = result['description'] if 'description' in result else None
    brand = result['brand'] if 'brand' in result else None
    try:
        created_item = create_item(
            name=name,
            image=image,
            author_id=author_id,
            description=description,
            brand=brand
        )
    except Exception as err:
        print('[created_item call]', err)
        return {"err": str(err)}, 400
    return {"msg": created_item.json()}


@bp.route('/items/<int:item_id>', methods=['GET'])
@protected_route
def items_get_by_id(item_id):
    if item_id is None:
        return {"err": "You should provide and item id!"}, 400
    found_item = get_item_by_id(item_id)
    if found_item is None:
        return {"err": "Item was not found!"}, 404
    return {"item": found_item.json()}


@bp.route('/items/<int:item_id>', methods=['DELETE'])
@protected_route
def items_delete(item_id):
    try:
        delete_item(item_id)
    except Exception as err:
        return {"err": str(err)}
    return {"msg": "Item deleted successfully"}


@bp.route('/items/<int:item_id>', methods=['PATCH'])
@protected_route
def items_edit(item_id):
    schema = UpdateItemSchema()
    json_request = request.json
    if json_request is None:
        return {"err": "you should provide at least 1 parameter to change"}
    error = schema.validate(json_request)
    if error:
        return {"err": error}

    try:
        update_item(item_id=item_id, **json_request)
    except Exception as err:
        print(err)
        return {"err": str(err)}
    return {"item": "item"}


@bp.route('/items/<string:query>')
@protected_route
def items_search(query):
    if len(query) < 3:
        return {"err": "search query must be atleast 3 characters long!"}, 400

    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 20)

    result = search_items(query=query, offset=offset, limit=limit)
    return {"items": result}
