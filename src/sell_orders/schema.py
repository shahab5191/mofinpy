from enum import Enum
from marshmallow import Schema, fields


class SellOrderStates(Enum):
    Ordered = "ordered",
    Shipped = "shipped",
    Recieved = "recieved",
    Canceled = "canceled"


class CreateSellOrderSchema(Schema):
    inventory_id = fields.Integer(required=True)
    customer_id = fields.Integer(required=True)
    payment = fields.Float(required=True)
    currency_id = fields.Integer(required=True)
    state = fields.Enum(SellOrderStates)
    creation_date = fields.DateTime()
    update_date = fields.DateTime()


class UpdateSellOrderSchema(Schema):
    inventory_id = fields.Integer()
    customer_id = fields.Integer()
    payment = fields.Float()
    currency_id = fields.Integer()
    state = fields.Enum(SellOrderStates)
    creation_date = fields.DateTime()
    update_date = fields.DateTime()
