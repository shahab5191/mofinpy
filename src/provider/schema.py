from marshmallow import Schema, fields


class CreateProviderSchema(Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    tel = fields.String(required=True)
    contact_person = fields.String(required=True)
    currency_id = fields.Integer(required=True)
    location_id = fields.Integer(required=True)
    website = fields.Url()
    createion_date = fields.DateTime()
    update_date = fields.DateTime()
