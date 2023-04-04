from marshmallow import fields, Schema, INCLUDE, EXCLUDE


class SMCUpdateReleasedContractRequestSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    _id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    highlight_text = fields.Str(allow_none=True)
    image_url = fields.Str(allow_none=True)
    social_link = fields.Dict(allow_none=True)


class SMCUpdateReleasedContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = fields.Str(required=True)
    result = fields.Bool(required=True)
