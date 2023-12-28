from marshmallow import Schema, fields


class CreateCurrencySchema(Schema):
    unit = fields.String(required=True)


class UpdateCurrencySchema(Schema):
    unit = fields.String()
