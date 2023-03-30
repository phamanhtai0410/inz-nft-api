# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas import SMCSignatureResponseSchema, SMCSignatureSchema
from services.smc.signature import SMCSignatureService


class SMCSignatureResource(Resource):

    @security.http(
        form_data=SMCSignatureSchema(),
        response=SMCSignatureResponseSchema()
    )
    def post(self, form_data):
        _signature_data = SMCSignatureService.create_signature(form_data=form_data)
        return _signature_data
        # return _response
