from marshmallow import Schema, fields


class HelloSchema(Schema):
    info = fields.String()