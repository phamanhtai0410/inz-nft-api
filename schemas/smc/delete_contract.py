from marshmallow import fields, Schema, INCLUDE, EXCLUDE


class SMCDeleteContractRequestSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    contract_id = fields.Str(required=True)


class SMCDeleteContractResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = fields.Str(required=True)
    result = fields.Bool(required=True)
