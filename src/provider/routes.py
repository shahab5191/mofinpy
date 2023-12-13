from flask import g, request
from src.provider import bp
from src.provider.functions import create_provider, get_providers
from src.provider.schema import CreateProviderSchema
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
        data = schema.load(json_data)
    except Exception as err:
        print(err)
        return {"err": str(err)}

    try:
        created_provider = create_provider(
            authord_id=g.user_data['id'], **data)
    except Exception as err:
        print(err)
        return {"err": str(err)}

    return {"provider": created_provider.json()}
