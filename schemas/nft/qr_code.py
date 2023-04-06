from marshmallow import Schema, EXCLUDE, fields, RAISE, validate, post_dump
from enums.qr_code import QrCodeAction
from lib import ObjectIdField, Chains


class QrCodeRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    contract_address = fields.String(required=True)
    index_type = fields.Integer(required=True)
    amount = fields.Integer(allow_none=True)
    act = fields.String(
        validate=validate.OneOf([
            QrCodeAction.MINT
        ]),
        required=True
    )

    @post_dump
    def post_dump_qr(self, data, **kwargs):
        data['contract_address'] = data['contract_address'].lower()

        return data

class QrCodeResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    qr_image_url = fields.String()


