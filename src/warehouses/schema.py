from marshmallow import Schema, fields


class CreateWarehouseSchema(Schema):
    name = fields.String(required=True)
    location_id = fields.Integer(required=True)
    creation_date = fields.DateTime()
    update_date = fields.DateTime()


class UpdateWarehouseSchema(Schema):
    name = fields.String()
    location_id = fields.Integer()
    creation_date = fields.DateTime()
    update_date = fields.DateTime()
