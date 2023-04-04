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


class NFTsResource(Resource):

    @security.http(
        params=NFTsRequestSchema(),
        response=NFTsResponseSchema()
    )
    def get(self, params):

        _page = get(params, 'page', default=1)
        _page_size = get(params, 'page_size', default=10)
        _chain = get(params, 'chain', default=None)
        _sort_field = get(params, 'sort_field', default=None)
        _sort_type = get(params, 'sort_type', default=None)
        _contracts = request.args.getlist('contract[]', str)

        _response = NFTsServices.get_nfts(
            page=_page,
            page_size=_page_size,
            chain=_chain,
            contracts=_contracts,
            sort_field=_sort_field,
            sort_type=_sort_type
        )

        return _response
