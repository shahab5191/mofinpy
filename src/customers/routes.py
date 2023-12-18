from flask import g, request
from src.customers import bp
from src.customers.functions import create_customer, delete_customer, list_customers, update_customer
from src.customers.schema import CreateCustomerSchema, UpdateCustomerSchema
from src.utils.pagination import pagination_return_format
from src.utils.protect_route import protected_route


@bp.route('/customers/', methods=['GET'])
@protected_route
def customers_list():
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    result = list_customers(limit=limit, offset=offset)

    return pagination_return_format(
        items=result['arr'],
        count=result['count'],
        offset=offset
    )


@bp.route('/customers/', methods=['POST'])
@protected_route
def customer_create():
    json_data = request.json
    if json_data is None:
        return {"err": "You should provide Customer data in json format!"}, 400

    schema = CreateCustomerSchema()
    errors = schema.validate(json_data)
    if errors:
        return {"err": errors}, 400

    try:
        created_customer = create_customer(
            g.user_data['id'],
            **json_data
        )
    except Exception as err:
        print('[create_customer]', err)
        return {"err": str(err)}, 500

    return {"customer": created_customer}, 201


@bp.route('/customers/<int:id>', methods=['PATCH'])
@protected_route
def customer_update(id):
    json_data = request.json
    if json_data is None:
        return {"err": "You should provide Customer data in json format!"}, 400
    schema = UpdateCustomerSchema()
    errors = schema.validate(json_data)
    print(errors)
    if errors:
        return {"err": errors}, 400

    try:
        updated_customer = update_customer(
            id=id,
            **json_data
        )
    except Exception as err:
        print(err)
        return {"err": str(err)}, 500

    return {"customer": updated_customer}, 201


@bp.route('/customers/<int:id>', methods=['DELETE'])
@protected_route
def customer_delete(id):
    try:
        delete_customer(id)
    except Exception as err:
        print('[delete_customer]', err)
        return {"err": str(err)}, 500

    return {"msg": f'customer with id:{id} deleted successfully!'}
