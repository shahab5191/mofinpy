from flask import request
from sqlalchemy import func, select
from src.history import bp
from src.history.schema import GetHistorySchema
from src.models.history import History
from src.utils.pagination import pagination_return_format
from src.utils.protect_route import protected_route
from src.extensions import db


@bp.route('/history/', methods=['GET'])
@protected_route
def history_get():
    json_data = request.json
    if json_data is None:
        return {"err": "You should provide data to get history"}, 400

    schema = GetHistorySchema()
    errors = schema.validate(json_data)

    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    if errors:
        return {"err": "Please provide valid data!"}, 400
    history = History.query.where(
        History.model_name == json_data['model']).where(
        History.record_id == json_data['id']).order_by(
        History.creation_date).limit(limit).offset(offset).all()
    count = db.session.scalar(
        select(func.count()).
        select_from(History).
        filter(History.model_name == json_data['model']).
        filter(History.record_id == json_data['id'])
    )
    return pagination_return_format(
        count=count,
        items=history,
        offset=offset
    )
