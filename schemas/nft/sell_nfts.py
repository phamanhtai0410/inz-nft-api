from marshmallow import Schema, EXCLUDE, fields, RAISE, validate, ValidationError
from lib import ObjectIdField, Chains, NotBlank
from lib.schema import DatetimeField



def validate_price(n):
    if n <= 0:
        raise ValidationError('Price must be greater than 0.')

class SellNftsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nft_id = ObjectIdField(required=True)
    # NOTE: in day
    buy_deadline = fields.Integer(required=True, validate=validate.OneOf([
        7,
        30,
        90
    ]))
    currency_address = fields.String(required=True)
    price = fields.Float(required=True, validate=validate_price)

