from src.items import bp
from src.items.functions import search_items
from src.items.schemas import CreateItemSchema, UpdateItemSchema
from src.models.item import Item
from src.utils.protect_route import protected_route
from flask import g, request
from src.utils.crud import CRUD


crud = CRUD(model=Item,
            create_schema=CreateItemSchema(),
            update_schema=UpdateItemSchema(),
            name="Item"
            )


@bp.route('/items/', methods=['GET'])
@protected_route
def items():
    return crud.get_all(request.args)


@bp.route('/items/', methods=['POST'])
@protected_route
def items_create():
    return crud.create(user_id=g.user_data['id'],
                       data=request.json
                       )


@bp.route('/items/<int:id>', methods=['GET'])
@protected_route
def items_get_by_id(id):
    return crud.get(id)


@bp.route('/items/<int:id>', methods=['DELETE'])
@protected_route
def items_delete(id):
    return crud.delete(id, user_id=g.user_data['id'])


@bp.route('/items/<int:id>', methods=['PATCH'])
@protected_route
def items_edit(id):
    return crud.update(id=id,
                       user_id=g.user_data['id'],
                       data=request.json
                       )

# TODO: Move search to crud class


@bp.route('/items/<string:query>')
@protected_route
def items_search(query):
    if len(query) < 3:
        return {"err": "search query must be atleast 3 characters long!"}, 400

    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 20)

    result = search_items(query=query, offset=offset, limit=limit)
    return {"items": result}
