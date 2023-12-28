from marshmallow import Schema, ValidationError, fields, validates


class CreateItemSchema(Schema):
    name = fields.String(required=True)
    image_id = fields.Integer()
    description = fields.String()
    brand = fields.String()

    @validates('name')
    def validate_name(self, value):
        min = 4
        if len(value) < min:
            raise ValidationError(
                f'Name should have more than {min} characters')

    @validates('description')
    def validate_description(self, value):
        if value is None:
            return
        min = 4
        if len(value) < min:
            raise ValidationError(
                f'Description should have more than {min} characters')


class UpdateItemSchema(Schema):
    name = fields.String()
    image_id = fields.Integer()
    description = fields.String()
    brand = fields.String()

    @validates('name')
    def validate_name(self, value):
        if value is None:
            return
        min = 4
        if len(value) < min:
            raise ValidationError(
                f'Name should have more than {min} characters')

    @validates('description')
    def validate_description(self, value):
        if value is None:
            return
        min = 4
        if len(value) < min:
            raise ValidationError(
                f'Description should have more than {min} characters')
