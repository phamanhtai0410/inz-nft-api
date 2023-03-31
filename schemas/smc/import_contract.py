from marshmallow import Schema, EXCLUDE, fields, RAISE, validate, INCLUDE
from enums.contract import ContractMethod
from enums.order import Currency
from helper.validator import is_valid_number, is_valid_subdomain
from lib import Chains, TokenStandard, IsObjectId, DatetimeField, ObjectIdField
from schemas.smc.create_contract import ContractDescriptionSchema, NFTOfContractSchema


class SMCImportContractRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    contract = fields.String(required=True)
    name = fields.String(allow_none=True)
    symbol = fields.String(allow_none=True)
    chain = fields.String(required=True, validate=validate.OneOf([
        Chains.BSC,
        Chains.ETHEREUM
    ]))
    # currency = fields.String(required=True, validate=validate.OneOf([
    #     Currency.BUSD,
    #     Currency.USDT,
    #     Currency.INZ,
    # ]))
    # standard = fields.String(required=True, validate=validate.OneOf([
    #     TokenStandard.ERC721,
    #     TokenStandard.ERC1155
    # ]))
    image_url = fields.Str(allow_none=True)
    template_id = fields.String(required=True, validate=IsObjectId())
    highlight_text = fields.Str(allow_none=True, default='')
    # social_link = fields.Dict(allow_none=True, default={})
    # nft_list = fields.List(fields.Nested(NFTOfContractSchema()), default=[])


class SMCImportContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    result = fields.Bool(required=True)
