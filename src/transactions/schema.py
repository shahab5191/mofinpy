from marshmallow import Schema, fields


class CreateTransactionSchema(Schema):
    currency_id = fields.Integer(required=True)
    amount = fields.Float(required=True)


class UpdateTransactionSchema(Schema):
    currency_id = fields.Integer()
    amount = fields.Float()
