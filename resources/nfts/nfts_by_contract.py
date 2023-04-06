# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get
from flask import request

from connect import security
from schemas import NFTsByContractRequestSchema
from services import MoralisServices


class NFTsByContractResource(Resource):

    @security.http(
        params=NFTsByContractRequestSchema(),
        # response=NFTsBYContractResponseSchema()
    )
    def get(self, params):
        _chain = get(params, 'chain')
        _contract_address = get(params, 'contract_address')

        _result = MoralisServices.get_nfts_list(chain=_chain, contract_address=_contract_address)

        return {
            'nfts': get(_result, 'result', [])
        }
