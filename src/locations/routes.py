from flask import g, request
from src.locations import bp
from src.locations.functions import create_location, delete_location, list_locations, update_location
from src.locations.schema import CreateLocationSchema, UpdateLocationSchema
from src.utils.pagination import pagination_return_format
from src.utils.protect_route import protected_route


@bp.route('/locations/', methods=['GET'])
@protected_route
def locations_list():
    offset = request.args.get('offset') or 0
    limit = request.args.get('limit') or 10

    try:
        result = list_locations(offset=offset, limit=limit)
    except Exception as err:
        print('[location_list]', err)
        return {"err": str(err)}

    return pagination_return_format(
        items=result['arr'],
        count=result['count'],
        offset=offset
    )


@bp.route('/locations/', methods=['POST'])
@protected_route
def location_create():
    json_data = request.json
    if json_data is None:
        return {"err": "You must provide Location data!"}, 400

    schema = CreateLocationSchema()
    errors = schema.validate(json_data)
    if errors:
        return {"err": "Data provided are not valid!"}, 400

    try:
        new_location = create_location(
            author_id=g.user_data['id'],
            **json_data
        )
    except Exception as err:
        print('[location_create]', err)
        return {"err": str(err)}, 500

    return {"location": new_location}, 201


@bp.route('/locations/<int:id>', methods=['PATCH'])
@protected_route
def location_update(id):
    json_data = request.json
    if json_data is None:
        return {"err": "You must provide Location data!"}, 400
    schema = UpdateLocationSchema()
    errors = schema.validate(json_data)
    if errors:
        return {"err": errors}, 400
    try:
        updated_location = update_location(id, **json_data)
    except Exception as err:
        print('[update_location]', err)
        return {"err": str(err)}, 404

    return {"location": updated_location}, 201


@bp.route('/locations/<int:id>', methods=['DELETE'])
@protected_route
def location_delete(id):

    try:
        delete_location(id)
    except Exception as err:
        return {"err": err}, 404

    return {"msg": f'Location with id:{id} deleted successfully'}
