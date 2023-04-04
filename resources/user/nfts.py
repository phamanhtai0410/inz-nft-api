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
from schemas import NFTsRequestSchema, NFTsResponseSchema
from services import NFTsServices


class UserNFTsResource(Resource):

    @security.http(
        params=NFTsRequestSchema(),
        response=NFTsResponseSchema(),
        login_required=True
    )
    def get(self, params, login_info):
        _contracts = request.args.getlist('contract[]', str)

        _response = NFTsServices.get_user_nfts(user_id=get(login_info, 'user._id'), params={
            **params,
            'contracts': _contracts
        })

        return _response

