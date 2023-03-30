from marshmallow import Schema, EXCLUDE, fields, RAISE, validate
from lib import ObjectIdField, DatetimeField

class SMCSignatureSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    chain_id = fields.Integer(required=True)
    user_address = fields.String(required=True)
    contract_address = fields.String(required=True)
    nft_address = fields.String(required=True)
    nft_type = fields.Integer(required=True)
    # discount = fields.Float(default=0, missing=0)
    # is_whitelist = fields.Boolean(default=False, missing=False)
    amount = fields.Integer(required=True, validate=validate.Range(min=1))

class SMCSignatureResponseObj(SMCSignatureSchema):
    discount = fields.Float(default=0, missing=0)
    is_whitelist = fields.Boolean(default=False, missing=False)
    callback = fields.String(required=True)


class SMCSignatureResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    signature = fields.String()
    data = fields.Nested(SMCSignatureResponseObj)