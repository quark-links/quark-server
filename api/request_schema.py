from marshmallow import Schema, fields


class CreateShortLinkSchema(Schema):
    url = fields.Url(required=True)