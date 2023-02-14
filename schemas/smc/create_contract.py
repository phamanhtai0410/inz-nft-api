from marshmallow import Schema, EXCLUDE, fields, RAISE, validate
from lib import Chains, TokenStandard, IsObjectId


class SMCCreateContractRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.String(required=True)
    symbol = fields.String(required=True)
    total_supply = fields.Integer(required=True)
    royalty = fields.Float(required=True)
    chain = fields.String(required=True, validate=validate.OneOf([
        Chains.BSC,
        Chains.ETHEREUM
    ]))
    standard = fields.String(required=True, validate=validate.OneOf([
        TokenStandard.ERC721,
        TokenStandard.ERC1155
    ]))
    image = fields.String(required=True)
    template_id = fields.String(required=True, validate=IsObjectId())


class SMCCreateContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    id = fields.String(data_key='id', required=True)
