from marshmallow import Schema, EXCLUDE, fields, RAISE
from lib import ObjectIdField, DatetimeField
from schemas.smc.create_contract import ContractDescriptionSchema, NFTOfContractSchema


class TemplateCategorySchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    name = fields.String(required=True)
    is_active = fields.Boolean(required=True, default=True)


class TemplateSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    thumbnail = fields.String(required=True)
    images = fields.List(fields.String, required=True)
    price = fields.Float(required=True)
    author = fields.String(required=True)
    author_image = fields.String(required=True)
    meta = fields.Dict(required=False, default={})
    created_time = DatetimeField(required=True)


class ContractsRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    page = fields.Integer(required=False, default=1, allow_none=True)
    page_size = fields.Integer(required=False, default=10, allow_none=True)


class ContractsSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    template = fields.Nested(TemplateSchema(only=('_id', 'title', 'description', 'thumbnail', 'price', 'author')))
    category = fields.Nested(TemplateCategorySchema(only=('_id', 'name')))
    contract = fields.String(required=True)
    name = fields.String(required=True)
    symbol = fields.String(required=True)
    total_supply = fields.Integer(required=True)
    total_raise = fields.Float(required=True)
    chain = fields.String(required=True)
    currency = fields.String(required=True)
    currency_address = fields.String(required=True)
    standard = fields.String(required=True)
    description = fields.List(fields.Nested(ContractDescriptionSchema()), allow_none=True, missing=[])
    about_owner = fields.Str(allow_none=True)
    owner_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(required=True)
    highlight_text = fields.Str(allow_none=True)
    max_allocation = fields.Int(allow_none=True)
    start_time = DatetimeField(required=True)
    end_time = DatetimeField(required=True)
    website_domain = fields.List(fields.Str(required=True), default=[], missing=[])
    full_domain = fields.List(fields.Str(required=True), default=[], missing=[])
    social_link = fields.Dict(allow_none=True)
    contract_method = fields.Int(required=True)
    is_box = fields.Bool(required=True)
    is_fixed_token = fields.Bool(required=True)
    nft_list = fields.List(fields.Nested(NFTOfContractSchema()))
    type = fields.String(required=True)
    deploy_address = fields.String(required=False, missing='')
    factory_address = fields.String(required=False, missing='')
    dapp_creator_address = fields.String(required=False, missing='')
    is_deleted = fields.Bool(required=True)
    deleted_time = DatetimeField(required=False, missing=None)
    is_released = fields.Bool(required=True)
    created_time = DatetimeField(required=True)


class ContractsResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(ContractsSchema()), data_key='items', missing=[])
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)
