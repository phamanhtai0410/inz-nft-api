# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.nfts.nfts import NFTsResource
from resources.nfts.qr_metamask import QrMetamaskResource
from resources.nfts.nfts_by_contract import NFTsByContractResource

nfts_resources = {
    '/list': NFTsResource,
    '/import': NFTsByContractResource,
    '/qr/metamask': QrMetamaskResource,
}
