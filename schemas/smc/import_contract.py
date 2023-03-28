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
    name = fields.String(required=True)
    symbol = fields.String(required=True)
    total_supply = fields.Integer(required=True, validate=is_valid_number)
    total_raise = fields.Float(required=True, validate=is_valid_number)
    chain = fields.String(required=True, validate=validate.OneOf([
        Chains.BSC,
        Chains.ETHEREUM
    ]))
    currency = fields.String(required=True, validate=validate.OneOf([
        Currency.BUSD,
        Currency.USDT,
        Currency.INZ,
    ]))
    standard = fields.String(required=True, validate=validate.OneOf([
        TokenStandard.ERC721,
        TokenStandard.ERC1155
    ]))
    description = fields.List(fields.Nested(ContractDescriptionSchema()), allow_none=True, default=[])
    about_owner = fields.Str(allow_none=True, default='')
    owner_image_url = fields.Str(allow_none=True, default='')
    image_url = fields.Str(required=True)
    template_id = fields.String(required=True, validate=IsObjectId())
    highlight_text = fields.Str(allow_none=True, default='')
    start_time = DatetimeField(required=True)
    end_time = DatetimeField(required=True)
    website_domain = fields.Str(required=True, validate=is_valid_subdomain)
    social_link = fields.Dict(allow_none=True, default={})
    contract_method = fields.Int(required=True, validate=validate.OneOf([
        ContractMethod.USER_WALLET,
        ContractMethod.INZ_WALLET
    ]))
    is_box = fields.Bool(required=True)
    is_fixed_token = fields.Bool(required=False, default=False)
    nft_list = fields.List(fields.Nested(NFTOfContractSchema()), default=[])
    price = fields.Float(required=True, validate=is_valid_number)


class SMCImportContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    result = fields.Bool(required=True)
