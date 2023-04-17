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
    discount = fields.Integer(default=0, missing=0)
    is_whitelist = fields.Boolean(default=False, missing=False)
    callback = fields.String(required=True)


class SMCSignatureResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    signature = fields.String()
    deadline = fields.Int()
    data = fields.Nested(SMCSignatureResponseObj)

class SMCSignatureBuyNftRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    chain_id = fields.Integer(required=True)
    to_address = fields.String(required=True)
    nft_id = ObjectIdField(required=True)

class SMCSignatureBuyNftResponseObj(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    order_id = fields.Integer(required=True)
    from_to = fields.List(fields.String, validate=validate.Length(equal=2))
    nft_and_token = fields.List(fields.String, validate=validate.Length(equal=2))
    id_and_amount = fields.List(fields.Integer, validate=validate.Length(equal=2))
    additional_token_receivers = fields.List(fields.String, default=[], missing=[])
    all_amounts = fields.List(fields.Integer, validate=validate.Length(min=1))

class SMCSignatureBuyNftResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    signature = fields.String(required=True)
    deadline = fields.Integer(required=True)
    data = fields.Nested(SMCSignatureBuyNftResponseObj)
