def pagination_return_format(items, count, offset):
    json_items = [item.json() for item in items]
    return {
        "items": json_items,
        "pagination": {
            "total": count,
            "left": count - (offset + len(json_items)),
            "count": len(json_items)
        }
    }
