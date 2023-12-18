from flask import g, request
from src.models.provider import Provider
from src.provider import bp
from src.provider.schema import CreateProviderSchema, UpdateProviderSchema
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route


crud = CRUD(Provider,
            create_schema=CreateProviderSchema(),
            update_schema=UpdateProviderSchema(),
            name="Provider"
            )


@bp.route('/providers/', methods=['GET'])
@protected_route
def provider_get():
    return crud.get_all(request.args)


@bp.route('/providers/', methods=['POST'])
@protected_route
def provider_create():
    return crud.create(
        author_id=g.user_data['id'],
        data=request.json
    )


@bp.route('/providers/<int:id>', methods=['GET'])
@protected_route
def provider_get_by_id(id):
    return crud.get(id)


@bp.route('/providers/<int:id>', methods=['PATCH'])
@protected_route
def provider_update(id):
    return crud.update(id, request.json)


@bp.route('/providers/<int:id>', methods=['DELETE'])
@protected_route
def provider_delete(id):
    return crud.delete(id)
