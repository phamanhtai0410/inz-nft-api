from marshmallow import Schema, EXCLUDE, fields, validate
from lib import ObjectIdField, SUPPORTED_CHAINS
from lib.schema import DatetimeField


class NFTsRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    page = fields.Integer(required=False, default=1, allow_none=True)
    page_size = fields.Integer(required=False, default=10, allow_none=True)
    chain = fields.String(validate=validate.OneOf(SUPPORTED_CHAINS), allow_none=True)
    sort_field = fields.String(allow_none=True)
    sort_type = fields.String(validate=validate.OneOf([
        'desc',
        'asc'
    ]), allow_none=True)


class NFTSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    contract = fields.String(required=True)
    token_id = fields.Integer(required=True)
    on_market = fields.Boolean(required=True)
    type = fields.Integer(required=True)
    metadata_link = fields.String(default='', missing='', allow_none=True)
    user = ObjectIdField()
    image_url = fields.String(default='', missing='', allow_none=True)
    price = fields.Float(default=0, missing=0)
    name = fields.String(default='', missing='')
    buy_deadline = DatetimeField(allow_none=True)
    currency_address= fields.String(required=True)
    chain_id = fields.Integer(required=True)
    chain = fields.String(required=True)
    properties = fields.Raw(default=[], missing=[])
    actions = fields.Raw(default=[], missing=[])
    standard = fields.String(allow_none=True)
    highlight_text = fields.String(allow_none=True)
    order_id = fields.Integer(allow_none=True)
    # buy_signature = fields.String(allow_none=True)


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
    items = fields.List(fields.Nested(NFTSchema()), data_key='items', missing=[])
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)
