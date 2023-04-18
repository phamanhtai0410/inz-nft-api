from marshmallow import Schema, EXCLUDE, fields, RAISE, validate, post_dump
from enums.qr_code import QrCodeAction
from lib import ObjectIdField, Chains


class UsersSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = ObjectIdField(allow_none=True)
    username = fields.String(allow_none=True)
    public_address = fields.String(allow_none=True)
    avatar = fields.String(allow_none=True)




