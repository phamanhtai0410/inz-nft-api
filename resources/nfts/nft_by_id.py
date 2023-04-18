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
from schemas.nft import NFTSchema
from services.nft import NFTsServices


class NFTsByIdResource(Resource):

    @security.http(
        response=NFTSchema()
    )
    def get(self, nft_id):

        _result = NFTsServices.get_nft_by_id(nft_id=nft_id)

        return _result