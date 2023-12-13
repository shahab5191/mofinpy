from marshmallow import Schema, fields


class CreatePurchaseSchema(Schema):
    item_id = fields.Integer(required=True)
    price = fields.Float(required=True)
    currency_id = fields.Integer(required=True)
    to_rial_rate = fields.Float(required=True)
    quantity = fields.Integer()
    provider_id = fields.Integer(required=True)
    order_date = fields.DateTime(required=False)
    update_date = fields.DateTime(required=False)
    make_unique = fields.Boolean(required=True)
