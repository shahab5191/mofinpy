from flask import g, request
from src.models.warehouse import Warehouse
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route
from src.warehouses import bp
from src.warehouses.schema import CreateWarehouseSchema, UpdateWarehouseSchema


crud = CRUD(model=Warehouse,
            create_schema=CreateWarehouseSchema(),
            update_schema=UpdateWarehouseSchema(),
            name="Warehouse"
            )


@bp.route('/warehouses/', methods=['GET'])
@protected_route
def warehouses_list():
    return crud.get_all(request.args)


@bp.route('/warehouses/', methods=['POST'])
@protected_route
def warehouses_create():
    return crud.create(user_id=g.user_data['id'],
                       data=request.json
                       )


@bp.route('/warehouses/<int:id>', methods=['PATCH'])
@protected_route
def warehouse_update(id):
    return crud.update(id=id,
                       user_id=g.user_data['g'],
                       data=request.json
                       )


@bp.route('/warehouses/<int:id>', methods=['DELETE'])
@protected_route
def warehouse_delete(id):
    return crud.delete(id, user_id=g.user_data['id'])
