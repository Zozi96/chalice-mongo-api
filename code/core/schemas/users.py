from marshmallow import fields
from core.schemas import MongoBaseSchema


class UserSchema(MongoBaseSchema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    first_name = fields.String()
    last_name = fields.String()
