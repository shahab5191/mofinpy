from flask import g, request
from src.models.purchase_order import PurchaseOrder
from src.purchase import bp
from src.purchase.functions import create_purchase, delete_purchase, update_purchase
from src.purchase.schemas import CreatePurchaseSchema, UpdatePurchaseSchema
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route


crud = CRUD(model=PurchaseOrder,
            create_schema=CreatePurchaseSchema(),
            update_schema=UpdatePurchaseSchema(),
            name="Purchase Order"
            )


@bp.route('/purchases/', methods=['GET'])
@protected_route
def purchases():
    return crud.get_all(request.args)


@bp.route('/purchases/', methods=['POST'])
@protected_route
def purchases_create():
    json_data = request.json
    if json_data is not None and 'state' in json_data and json_data['state'] == 'Received':
        schema = CreatePurchaseSchema()
        errors = schema.validate(json_data)
        if errors:
            return {"err": "please provide valid data"}, 400
        return create_purchase(author_id=g.user_data['id'],
                               **json_data)
    return crud.create(
        data=request.json,
        user_id=g.user_data['id']
    )


@bp.route('/purchases/<int:id>', methods=['PATCH'])
@protected_route
def purchase_update(id):
    json_data = request.json
    if json_data is None:
        return {"err": "You should provide some data"}, 404
    if 'state' in json_data and json_data['state'] == 'Received':
        schema = UpdatePurchaseSchema()
        errors = schema.validate(json_data)
        if errors:
            print('[purchase_update]', errors)
            return {"err": "please provide valid data"}, 400
        return update_purchase(id=id, **json_data)
    else:
        return crud.update(
            id=id,
            data=json_data,
            user_id=g.user_data['id']
        )


@bp.route('/purchases/<int:id>', methods=['DELETE'])
@protected_route
def purchase_delete(id):
    return delete_purchase(id)
