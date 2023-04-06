# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.nfts.nfts import NFTsResource
from resources.nfts.qr_metamask import QrMetamaskResource

nfts_resources = {
    '/list': NFTsResource,
    '/qr/metamask': QrMetamaskResource
}
