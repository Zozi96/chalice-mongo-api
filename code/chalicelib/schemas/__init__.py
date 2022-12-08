from marshmallow import Schema, fields


class MongoBaseSchema(Schema):
    id = fields.String(attribute='_id')

    class Meta:
        ordered = True
