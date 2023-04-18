# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.nfts.nfts import NFTsResource
from resources.nfts.qr_metamask import QrMetamaskResource
from resources.nfts.nfts_by_contract import NFTsByContractResource
from resources.nfts.sell_nfts import SellNftResource
from resources.nfts.cancel_sell_nft import CancelSellNftResource
from resources.nfts.nft_by_id import NFTsByIdResource

nfts_resources = {
    '/list': NFTsResource,
    '/import': NFTsByContractResource,
    '/qr/metamask': QrMetamaskResource,
    '/sell': SellNftResource,
    '/cancel_sell/<string:nft_id>': CancelSellNftResource,
    '/<string:nft_id>': NFTsByIdResource,
    
}
