from marshmallow import Schema, EXCLUDE, fields, validate

from lib import Chains, NotBlank


class NFTsByContractRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # page = fields.Integer(required=False, default=1, allow_none=True)
    # page_size = fields.Integer(required=False, default=10, allow_none=True)
    chain = fields.String(required=True, validate=validate.OneOf([
        Chains.BSC,
        Chains.ETHEREUM
    ]))
    contract_address = fields.String(required=True, validate=NotBlank())


# class NFTsByContractResponseSchema(Schema):
#     class Meta:
#         unknown = EXCLUDE
#
#     # page = fields.Integer(required=False, default=1, allow_none=True)
#     # page_size = fields.Integer(required=False, default=10, allow_none=True)
#     result
