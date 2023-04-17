# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas.smc.signature import SMCSignatureBuyNftResponseSchema, SMCSignatureResponseSchema, SMCSignatureBuyNftRequestSchema
from services.smc.signature import SMCSignatureService


class SMCSignatureBuyNftResource(Resource):

    @security.http(
        form_data=SMCSignatureBuyNftRequestSchema(),
        response=SMCSignatureBuyNftResponseSchema()
    )
    def post(self, form_data):
        _signature_data = SMCSignatureService.create_buy_nft_signature(form_data=form_data)
        return _signature_data
        # return _response
