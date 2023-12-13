from flask import g, request
from src.purchase import bp
from src.purchase.functions import create_purchase, get_purchases
from src.purchase.schemas import CreatePurchaseSchema
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
        offset=offset)


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
