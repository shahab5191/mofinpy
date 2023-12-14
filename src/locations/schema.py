from marshmallow import Schema, fields


class CreateLocationSchema(Schema):
    country = fields.String()
    city = fields.String()
    address = fields.String(required=True)
    creation_date = fields.DateTime()
    update_date = fields.DateTime()


class UpdateLocationSchema(Schema):
    country = fields.String()
    city = fields.String()
    address = fields.String()
    creation_date = fields.DateTime()
    update_date = fields.DateTime()
