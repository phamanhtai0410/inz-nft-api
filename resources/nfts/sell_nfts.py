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
from schemas.nft.sell_nfts import SellNftsSchema
from services.nft.nft import NFTsServices


class SellNftResource(Resource):

    @security.http(
        form_data=SellNftsSchema(),
        login_required=True
    )
    def post(self, form_data, login_info):
        _response = NFTsServices.sell_nfts(user_id=get(login_info, 'user._id'), form_data=form_data)
        return _response
