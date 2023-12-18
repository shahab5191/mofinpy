from flask import g, request
from src.utils.pagination import pagination_return_format
from src.utils.protect_route import protected_route
from src.warehouses import bp
from src.warehouses.functions import create_warehouse, delete_warehouse, list_warehouses, update_warehouse
from src.warehouses.schema import CreateWarehouseSchema, UpdateWarehouseSchema


@bp.route('/warehouses/', methods=['GET'])
@protected_route
def warehouses_list():
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    result = list_warehouses(limit=limit, offset=offset)
    return pagination_return_format(
        items=result['arr'],
        count=result['count'],
        offset=offset
    )


@bp.route('/warehouses/', methods=['POST'])
@protected_route
def warehouses_create():
    json_data = request.json
    if json_data is None:
        return {"err": "You should provide Warehouse data!"}, 400

    schema = CreateWarehouseSchema()
    errors = schema.validate(json_data)
    if errors:
        return {"err": errors}, 400

    try:
        new_warehouse = create_warehouse(
            author_id=g.user_data['id'],
            **json_data
        )
    except Exception as err:
        print(err)
        return {"err": str(err)}, 500

    return {"warehouse": new_warehouse}, 201


@bp.route('/warehouses/<int:id>', methods=['PATCH'])
@protected_route
def warehouse_update(id):
    json_data = request.json
    if json_data is None:
        return {"err": "You should provide Warehouse data!"}, 400

    schema = UpdateWarehouseSchema()
    errors = schema.validate(json_data)
    if errors:
        return {"err": errors}, 404

    try:
        updated_warehouse = update_warehouse(id, **json_data)
    except Exception as err:
        print('[update_warehouse]', err)
        return {"err": str(err)}, 404

    return {"warehouse": updated_warehouse}


@bp.route('/warehouses/<int:id>', methods=['DELETE'])
@protected_route
def warehouse_delete(id):
    try:
        delete_warehouse(id)
    except Exception as err:
        print(['delete_warehouse'])
        return {'err': str(err)}, 500

    return {"msg": f'warehouse with id:{id} deleted successfully!'}
