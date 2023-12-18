from enum import Enum
from marshmallow import Schema, fields


class PurchaseOrderStates(Enum):
    Ordered = "Ordered"
    Shipped = "Shipped"
    Received = "Received"
    Canceled = "Canceled"


class CreatePurchaseSchema(Schema):
    item_id = fields.Integer(required=True)
    price = fields.Float(required=True)
    currency_id = fields.Integer(required=True)
    to_rial_rate = fields.Float(required=True)
    quantity = fields.Integer()
    provider_id = fields.Integer(required=True)
    cration_date = fields.DateTime(required=False)
    update_date = fields.DateTime(required=False)
    make_unique = fields.Boolean(required=True)
    state = fields.Enum(PurchaseOrderStates)
    warehouse_id = fields.Integer()


class UpdatePurchaseSchema(Schema):
    item_id = fields.Integer()
    price = fields.Float()
    currency_id = fields.Integer()
    to_rial_rate = fields.Float()
    quantity = fields.Integer()
    provider_id = fields.Integer()
    creation_date = fields.DateTime()
    update_date = fields.DateTime()
    make_unique = fields.Boolean()
    state = fields.Enum(PurchaseOrderStates)
    warehouse_id = fields.Integer()
