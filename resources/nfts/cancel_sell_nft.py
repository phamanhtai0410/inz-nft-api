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
from services.nft.nft import NFTsServices


class CancelSellNftResource(Resource):

    @security.http(
        login_required=True
    )
    def put(self, nft_id, login_info):
        _response = NFTsServices.cancel_sell_nfts(user_id=get(login_info, 'user._id'), nft_id=nft_id)
        return _response
