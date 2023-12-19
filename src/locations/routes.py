from flask import g, request
from src.locations import bp
from src.locations.schema import CreateLocationSchema, UpdateLocationSchema
from src.models.location import Location
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route


crud = CRUD(model=Location,
            create_schema=CreateLocationSchema(),
            update_schema=UpdateLocationSchema(),
            name='Location'
            )


@bp.route('/locations/', methods=['GET'])
@protected_route
def locations_list():
    return crud.get_all(request.args)


@bp.route('/locations/', methods=['POST'])
@protected_route
def location_create():
    return crud.create(user_id=g.user_data['id'],
                       data=request.json
                       )


@bp.route('/locations/<int:id>', methods=['PATCH'])
@protected_route
def location_update(id):
    return crud.update(id=id,
                       user_id=g.user_data['g'],
                       data=request.json
                       )


@bp.route('/locations/<int:id>', methods=['DELETE'])
@protected_route
def location_delete(id):
    return crud.delete(id=id,
                       user_id=g.user_data['id']
                       )
