from flask import g, request
from src.models.transactions import Transactions
from src.transactions import bp
from src.transactions.schema import CreateTransactionSchema, UpdateTransactionSchema
from src.utils.crud import CRUD
from src.utils.protect_route import protected_route


crud = CRUD(model=Transactions,
            create_schema=CreateTransactionSchema(),
            update_schema=UpdateTransactionSchema(),
            name='transactions'
            )


@bp.route('/transactions/', methods=['POST'])
@protected_route
def transactions_create():
    return crud.create(g.user_data['id'],
                       request.json
                       )
