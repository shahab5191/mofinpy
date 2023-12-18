from flask import g, request
from src.models.sell_order import SellOrder
from src.sell_orders import bp
from src.sell_orders.schema import CreateSellOrderSchema, UpdateSellOrderSchema
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route


crud = CRUD(SellOrder,
            create_schema=CreateSellOrderSchema(),
            update_schema=UpdateSellOrderSchema(),
            name="SellOrder"
            )


@bp.route('/sell_orders/', methods=['GET'])
@protected_route
def sell_orders_list():
    return crud.get_all(request.args)


@bp.route('/sell_orders/', methods=['POST'])
@protected_route
def sell_orders_create():
    return crud.create(
        author_id=g.user_data['id'],
        data=request.json
    )


@bp.route('/sell_orders/<int:id>', methods=['PATCH'])
@protected_route
def sell_orders_update(id):
    return crud.update(id, request.json)


@bp.route('/sell_orders/<int:id>', methods=['DELETE'])
@protected_route
def sell_orders_delete(id):
    return crud.delete(id)
