from marshmallow import Schema, EXCLUDE, fields, RAISE, validate, INCLUDE

from enums.contract import ContractMethod
from enums.order import Currency
from helper.validator import is_valid_number, is_valid_subdomain
from lib import Chains, TokenStandard, IsObjectId, DatetimeField


class NFTOfContractSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    name = fields.Str(required=True)
    image_uri = fields.Str(required=True)
    supply = fields.Int(required=True, validate=is_valid_number)
    price = fields.Float(allow_none=True, validate=is_valid_number)
    type = fields.Str(required=True)
    percent = fields.Float(allow_none=True)
    description = fields.Str(allow_none=True)


class ContractDescriptionSchema(Schema):
    title = fields.Str(required=True)
    html_content = fields.Str(required=True)
    image_uri = fields.Str(allow_none=True, missing='')


class SMCCreateContractRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.String(required=True)
    symbol = fields.String(required=True)
    total_supply = fields.Integer(required=True, validate=is_valid_number)
    total_raise = fields.Float(required=True, validate=is_valid_number)
    chain = fields.String(required=True, validate=validate.OneOf([
        Chains.BSC,
        Chains.ETHEREUM
    ]))
    currency = fields.String(required=True, validate=validate.OneOf([
        Currency.BNB,
        Currency.BUSD,
        Currency.USDT,
        Currency.ETH,
    ]))
    # standard = fields.String(required=True, validate=validate.OneOf([
    #     TokenStandard.ERC721,
    #     TokenStandard.ERC1155
    # ]))
    description = fields.List(fields.Nested(ContractDescriptionSchema()), allow_none=True, missing=[])
    about_owner = fields.Str(allow_none=True)
    owner_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(required=True)
    template_id = fields.String(required=True, validate=IsObjectId())
    highlight_text = fields.Str(allow_none=True)
    max_allocation = fields.Int(allow_none=True, validate=is_valid_number)
    start_time = DatetimeField(required=True)
    end_time = DatetimeField(required=True)
    website_domain = fields.Str(required=True, validate=is_valid_subdomain)
    social_link = fields.Dict(allow_none=True)
    contract_method = fields.Int(required=True, validate=validate.OneOf([
        ContractMethod.USER_WALLET,
        ContractMethod.INZ_WALLET
    ]))
    is_box = fields.Bool(required=True)
    is_fixed_token = fields.Bool(required=True)
    nft_list = fields.List(fields.Nested(NFTOfContractSchema()))


class SMCCreateContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str(required=True)
    is_released = fields.Bool(required=True)

