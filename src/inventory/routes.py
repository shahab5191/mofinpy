from flask import request
from src.inventory import bp
from src.inventory.functions import get_inventory_list
from src.utils.protect_route import protected_route


@bp.route('/inventory/', methods=['GET'])
@protected_route
def inventory_list():
    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 20)

    result = get_inventory_list(offset, limit)
    json_list = [item.json() for item in result['inventory']]
    return {
        "inventory": json_list,
        "pagination": {
            "total_records": result['count'],
            "records_left": result['count'] - (offset + len(json_list)),
            "records_count": len(json_list)
        }
    }
