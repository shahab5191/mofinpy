from marshmallow import Schema, fields


class CreateInventorySchema(Schema):
    item_id = fields.Integer(required=True)
    quantity = fields.Integer()
    creation_date = fields.DateTime()
    update_date = fields.DateTime()
    price = fields.Float(required=True)
    currency_id = fields.Integer(required=True)
    base_currency_rate = fields.Float(required=True)
    warehouse_id = fields.Integer(required=True)
    purchase_id = fields.Integer(required=True)


class UpdateInventorySchema(Schema):
    item_id = fields.Integer()
    quantity = fields.Integer()
    creation_date = fields.DateTime()
    update_date = fields.DateTime()
    price = fields.Float()
    currency_id = fields.Integer()
    base_currency_rate = fields.Float()
    warehouse_id = fields.Integer()
    purchase_id = fields.Integer()
