from flask import g, request
from src.provider import bp
from src.provider.functions import create_provider, delete_provider, get_providers, update_provider
from src.provider.schema import CreateProviderSchema, UpdateProviderSchema
from src.utils.pagination import pagination_return_format
from src.utils.protect_route import protected_route


@bp.route('/providers/', methods=['GET'])
@protected_route
def provider_get():
    offset = request.args.get('offset') or 0
    limit = request.args.get('limit') or 10
    result = get_providers(offset=offset, limit=limit)
    return pagination_return_format(
        items=result['arr'],
        count=result['count'],
        offset=offset
    )


@bp.route('/providers/', methods=['POST'])
@protected_route
def provider_create():
    json_data = request.json
    if not json_data:
        return {"err": "You should provide data"}, 400
    schema = CreateProviderSchema()
    errors = schema.validate(json_data)

    if errors:
        return {"err": errors}

    try:
        created_provider = create_provider(
            authord_id=g.user_data['id'],
            **json_data)
    except Exception as err:
        print(err)
        return {"err": str(err)}

    return {"provider": created_provider.json()}


@bp.route('/providers/<int:id>', methods=['PATCH'])
@protected_route
def provider_update(id):
    json_data = request.json

    if json_data is None:
        return {"err": "You should provide data to update"}, 400

    schema = UpdateProviderSchema()
    errors = schema.validate(json_data)
    if errors:
        return {"err": errors}, 400

    try:
        updated_provider = update_provider(id, **json_data)
    except Exception as err:
        print('[update_provider]', err)
        return {"err": str(err)}, 404

    return {"provider": updated_provider}


@bp.route('/providers/<int:id>', methods=['DELETE'])
@protected_route
def provider_delete(id):
    try:
        delete_provider(id)
    except Exception as err:
        return {"err": str(err)}, 404

    return {"msg": f"Provider with id:{id} deleted successfully!"}
