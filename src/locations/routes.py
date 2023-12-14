from flask import g, request
from src.locations import bp
from src.locations.functions import create_location, list_locations
from src.locations.schema import CreateLocationSchema
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
        return {"err", str(err)}, 500

    return {"location": new_location}, 201
