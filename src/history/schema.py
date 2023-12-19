from marshmallow import Schema, fields


class GetHistorySchema(Schema):
    model = fields.String(required=True)
    id = fields.Integer(required=True)
