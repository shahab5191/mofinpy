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


class UpdateProviderSchema(Schema):
    name = fields.String()
    email = fields.String()
    tel = fields.String()
    contact_person = fields.String()
    currency_id = fields.Integer()
    location_id = fields.Integer()
    website = fields.Url()
    creation_date = fields.DateTime()
    update_date = fields.DateTime()
