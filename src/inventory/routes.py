from flask import g, request
from src.inventory import bp
from src.inventory.schema import CreateInventorySchema, UpdateInventorySchema
from src.models.inventory import Inventory
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route


crud = CRUD(model=Inventory,
            update_schema=UpdateInventorySchema(),
            create_schema=CreateInventorySchema(),
            name="Inventory"
            )


@bp.route('/inventory/', methods=['GET'])
@protected_route
def inventory_list():
    return crud.get_all(request.args)


@bp.route('/inventory/', methods=['POST'])
@protected_route
def inventory_create():
    return crud.create(
        author_id=g.user_data['id'],
        data=request.json
    )


@bp.route('/inventory/<int:id>', methods=['PATCH'])
@protected_route
def inventory_update(id):
    return crud.update(id, request.json)


@bp.route('/inventory/<int:id>', methods=['DELETE'])
@protected_route
def inventory_delete(id):
    return crud.delete(id)
