# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas.nft.nfts import NFTsRequestSchema, NFTsResponseSchema
from services.nft.nft import NFTsServices


class NFTsResource(Resource):

    @security.http(
        params=NFTsRequestSchema(),
        response=NFTsResponseSchema(),
        is_blockchain=True
    )
    def get(self, params, contract):

        _page = get(params, 'page', default=1)
        _page_size = get(params, 'page_size', default=10)
        _chain = get(params, 'chain', default=None)
        _sort_price = get(params, 'sort_price', default=None)

        _response = NFTsServices.get_nfts(
            page=_page,
            page_size=_page_size,
            chain=_chain,
            contract=contract,
            sort_price=_sort_price
        )

        return _response
