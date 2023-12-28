from flask import g, request
from src.currency import bp
from src.currency.schema import CreateCurrencySchema, UpdateCurrencySchema
from src.models.currency import Currency
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route


crud = CRUD(model=Currency,
            create_schema=CreateCurrencySchema(),
            update_schema=UpdateCurrencySchema(),
            name='Currency'
            )


@bp.route('/currency/', methods=['GET'])
@protected_route
def currency_get_all():
    return crud.get_all(request.args)


@bp.route('/currency/<int:id>', methods=['GET'])
@protected_route
def currency_get(id):
    return crud.get(id)


@bp.route('/currency/', methods=['POST'])
@protected_route
def currency_create():
    return crud.create(user_id=g.user_data['id'],
                       data=request.json
                       )


@bp.route('/currency/<int:id>', methods=['PATCH'])
@protected_route
def currency_update(id):
    return crud.update(id=id,
                       user_id=g.user_data['id'],
                       data=request.json
                       )


@bp.route('/currency/<int:id>', methods=['DELETE'])
@protected_route
def currency_delete(id):
    return crud.delete(id=id, user_id=g.user_data['id'])
