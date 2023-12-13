from flask import g, request
from src.purchase import bp
from src.purchase.functions import create_purchase, delete_purchase, get_purchases, update_purchase
from src.purchase.schemas import CreatePurchaseSchema, UpdatePurchaseSchema
from src.utils.pagination import pagination_return_format
from src.utils.protect_route import protected_route


@bp.route('/purchases/', methods=['GET'])
@protected_route
def purchases():
    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 20)
    result = get_purchases(offset=offset, limit=limit)
    return pagination_return_format(
        items=result['arr'],
        count=result['count'],
        offset=offset
    )


@bp.route('/purchases/', methods=['POST'])
@protected_route
def purchases_create():
    json_data = request.json
    if not json_data:
        return {"err": "You should provide data"}, 400

    schema = CreatePurchaseSchema()
    errors = schema.validate(json_data)
    if errors:
        return {"err": errors}

    try:
        created_purchase = create_purchase(
            **json_data,
            author_id=g.user_data['id']
        )
    except Exception as err:
        print('[create_purchase]', err)
        return {"err": str(err)}, 400

    return {"item": created_purchase.json()}


@bp.route('/purchases/<int:id>', methods=['PATCH'])
@protected_route
def purchase_edit(id):
    json_data = request.json
    if json_data is None:
        return {"err": "You should provide some data"}
    schema = UpdatePurchaseSchema()
    errors = schema.validate(json_data)

    if errors:
        return {"err": errors}

    try:
        purchase = update_purchase(id, **json_data)
    except Exception as err:
        print('[update_purchase]:', err)
        return {"err": str(err)}

    return {"purchase": purchase.json()}


@bp.route('/purchases/<int:id>', methods=['DELETE'])
@protected_route
def purchase_delete(id):
    try:
        delete_purchase(id)
    except Exception as err:
        print('[purchase_delete]', err)
        return {"err": str(err)}

    return {"msg": "Item Removed successfully!"}
