from marshmallow import INCLUDE, Schema, fields, validate, EXCLUDE

# from enums.contract import ContractMethod
from enums.order import Currency
from helper.validator import is_valid_number, is_valid_subdomain
from lib import DatetimeField, Chains, IsObjectId, TokenStandard
from schemas.smc.create_contract import ContractDescriptionSchema, NFTOfContractSchema


class SMCUpdateNonReleasedContractRequestSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    _id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    # description = fields.List(fields.Nested(ContractDescriptionSchema()), allow_none=True)
    # about_owner = fields.Str(allow_none=True)
    # owner_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(required=True)
    highlight_text = fields.Str(allow_none=True)
    # max_allocation = fields.Int(allow_none=True, validate=is_valid_number)
    symbol = fields.Str(allow_none=True)
    chain = fields.String(required=False, allow_none=True, validate=validate.OneOf([
        Chains.BSC,
        Chains.ETHEREUM
    ]))
    currency = fields.String(required=False, allow_none=True, validate=validate.OneOf([
        Currency.BUSD,
        Currency.USDT,
        Currency.INZ,
    ]))
    # total_supply = fields.Int(allow_none=True, validate=is_valid_number)
    # total_raise = fields.Float(allow_none=True, validate=is_valid_number)
    # start_time = DatetimeField(allow_none=True)
    # end_time = DatetimeField(allow_none=True)
    website_domain = fields.Str(allow_none=True, validate=is_valid_subdomain)
    social_link = fields.Dict(allow_none=True)
    # contract_method = fields.Int(required=False, allow_none=True, validate=validate.OneOf([
    #     ContractMethod.USER_WALLET,
    #     ContractMethod.INZ_WALLET
    # ]))
    # is_box = fields.Bool(allow_none=True)
    # is_fixed_token = fields.Bool(required=True)
    nft_list = fields.List(fields.Nested(NFTOfContractSchema()), required=True)
    template_id = fields.String(required=False, allow_none=True, validate=IsObjectId())
    # standard = fields.String(required=False, allow_none=True, validate=validate.OneOf([
    #     TokenStandard.ERC721,
    #     TokenStandard.ERC1155
    # ]))


class SMCUpdateNonReleasedContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = fields.Str(required=True)
    result = fields.Bool(required=True)

