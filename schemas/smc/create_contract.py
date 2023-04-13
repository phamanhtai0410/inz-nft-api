from marshmallow import Schema, EXCLUDE, fields, RAISE, validate, INCLUDE

from enums.order import Currency
# from enums.contract import ContractMethod
from helper.validator import is_valid_number
from lib import IsObjectId, NotBlank, ObjectIdField, SUPPORTED_CHAINS


class MetadataPropertiesSchema(Schema):
    value = fields.Str(allow_none=True)
    trait_type = fields.Str(allow_none=True)
    display_type = fields.Str(allow_none=True, validate=validate.OneOf([
        'string', 'number', 'boost_percentage', 'boost_number', 'date'
    ]))


class MetadataActionsSchema(Schema):
    value = fields.Str(allow_none=True)
    action_type = fields.Str(allow_none=True)


class NFTOfContractSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    name = fields.Str(required=True, validate=NotBlank())
    image_url = fields.Str(required=True, validate=NotBlank())
    description = fields.Str(allow_none=True)
    supply = fields.Int(allow_none=True, validate=is_valid_number, missing=0)
    price = fields.Float(allow_none=True, validate=is_valid_number)
    type = fields.Str(allow_none=True)
    percent = fields.Float(allow_none=True)
    properties = fields.List(fields.Nested(MetadataPropertiesSchema()), allow_none=True, missing=[])
    actions = fields.List(fields.Nested(MetadataActionsSchema()), allow_none=True, missing=[])


class ContractDescriptionSchema(Schema):
    title = fields.Str(required=True, validate=NotBlank())
    html_content = fields.Str(required=True, validate=NotBlank())
    image_url = fields.Str(allow_none=True, missing='')


class SMCCreateContractRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.String(required=True, validate=NotBlank())
    symbol = fields.String(required=True, validate=NotBlank())
    # total_supply = fields.Integer(allow_none=True, validate=is_valid_number)
    # total_raise = fields.Float(allow_none=True, validate=is_valid_number)
    chain = fields.String(required=True, validate=validate.OneOf(SUPPORTED_CHAINS))
    currency = fields.String(required=True, validate=validate.OneOf([
        Currency.USDT,
    ]))
    # standard = fields.String(required=True, validate=validate.OneOf([
    #     TokenStandard.ERC721,
    #     TokenStandard.ERC1155
    # ]))
    # description = fields.List(fields.Nested(ContractDescriptionSchema()), allow_none=True, missing=[])
    # about_owner = fields.Str(allow_none=True)
    # owner_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(required=True, validate=NotBlank())
    user_template_id = fields.String(required=True, validate=IsObjectId())
    highlight_text = fields.Str(allow_none=True)
    # max_allocation = fields.Int(allow_none=True, validate=is_valid_number)
    # start_time = DatetimeField(allow_none=True)
    # end_time = DatetimeField(allow_none=True)
    # website_domain = fields.Str(required=True, validate=is_valid_subdomain)
    # social_link = fields.Dict(allow_none=True)
    # contract_method = fields.Int(allow_none=True, validate=validate.OneOf([
    #     ContractMethod.USER_WALLET,
    #     ContractMethod.INZ_WALLET
    # ]), missing=ContractMethod.USER_WALLET)
    # is_box = fields.Bool(required=True)
    # is_fixed_token = fields.Bool(required=True)
    nft_list = fields.List(fields.Nested(NFTOfContractSchema()), required=True)


class SMCCreateContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    name = fields.Str(required=True)
    symbol = fields.String(required=True)
    is_released = fields.Bool(required=True)
    chain = fields.String(required=True)
    currency = fields.String(required=True)
    image_url = fields.Str(required=True)
    highlight_text = fields.Str(allow_none=True)
    nft_list = fields.List(fields.Nested(NFTOfContractSchema()), required=True)
