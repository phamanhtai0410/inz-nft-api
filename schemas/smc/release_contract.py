from marshmallow import fields, Schema, INCLUDE, EXCLUDE
from lib import ObjectIdField, IsObjectId


class SMCReleaseContractRequestSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    contract_id = fields.Str(required=True, validate=IsObjectId())
    user_template_id = fields.Str(required=True, validate=IsObjectId())
    website_domain = fields.Str(required=True)


class SMCReleaseContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    domain = fields.Str(required=True)
    create_domain_status = fields.Str(required=True)
    create_smc_status = fields.Str(required=True)
