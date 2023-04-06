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
    user_template_id = fields.String(required=True, validate=IsObjectId())
    highlight_text = fields.Str(allow_none=True, default='')
    # social_link = fields.Dict(allow_none=True, default={})
    # nft_list = fields.List(fields.Nested(NFTOfContractSchema()), default=[])


class SMCImportContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    name = fields.Str(allow_none=True)
    contract = fields.Str(required=True)
    symbol = fields.String(allow_none=True)
    is_released = fields.Bool(required=True)
    chain = fields.String(required=True)
    image_url = fields.Str(required=True)
    highlight_text = fields.Str(allow_none=True)
