from marshmallow import Schema, EXCLUDE, fields, RAISE, validate

from enums.blockchain import Chains
from lib import ObjectIdField


class NFTsRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    page = fields.Integer(required=False, default=1, allow_none=True)
    page_size = fields.Integer(required=False, default=10, allow_none=True)
    chain = fields.String(required=True, validate=validate.OneOf([
        Chains.BSC_CHAIN,
        Chains.ETHEREUM_CHAIN
    ]), allow_none=True)
    sort_price = fields.String(required=False, validate=validate.OneOf([
        'desc',
        'asc'
    ]), allow_none=True)


class NftSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    contract = fields.String(required=True)
    token_id = fields.Integer(required=True)
    standard = fields.String(required=True)
    chain = fields.String(required=True)
    price = fields.String(required=True)
    amount = fields.Integer(required=True)
    metadata_link = fields.String(required=False, default='')
    metadata = fields.Dict(required=False, default={})
    images = fields.List(fields.String(), required=False, default=[])
    owner = fields.String(required=True)


class NFTsResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    # {
    #     "items": result,
    #     'num_of_page': num_of_page,
    #     'page_size': page_size,
    #     'page': page
    # }
    items = fields.List(fields.Nested(NftSchema), data_key='items', missing=[])
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)
