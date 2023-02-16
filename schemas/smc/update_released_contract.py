from marshmallow import fields, Schema, INCLUDE, EXCLUDE

from schemas.smc.create_contract import ContractDescriptionSchema


class SMCUpdateReleasedContractRequestSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    _id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    highlight_text = fields.Str(allow_none=True)
    description = fields.List(fields.Nested(ContractDescriptionSchema()), allow_none=True)
    about_owner = fields.Str(allow_none=True)
    owner_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(allow_none=True)
    social_link = fields.Dict(allow_none=True)


class SMCUpdateReleasedContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = fields.Str(required=True)
    result = fields.Bool(required=True)
