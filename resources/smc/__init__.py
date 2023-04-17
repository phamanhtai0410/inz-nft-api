# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.smc.create_contract import SMCCreateContractResource
from resources.smc.import_contract import SMCImportContractResource
from resources.smc.update_non_released_contract import SMCUpdateNonReleasedContractResource
from resources.smc.update_released_contract import SMCUpdateReleasedContractResource
from resources.smc.release_contract import SMCReleaseContractResource
from resources.smc.delete_contract import SMCDeleteContractResource
from resources.smc.contracts import ContractsResource
from resources.smc.signature import SMCSignatureResource
from resources.smc.signature_buy_nft import SMCSignatureBuyNftResource


smc_resources = {
    '/list': ContractsResource,
    '/create': SMCCreateContractResource,
    '/import': SMCImportContractResource,
    '/release': SMCReleaseContractResource,
    '/delete': SMCDeleteContractResource,
    '/update/non_released': SMCUpdateNonReleasedContractResource,
    '/update/released': SMCUpdateReleasedContractResource,
    '/signature': SMCSignatureResource,
    '/signature/buy_nft': SMCSignatureBuyNftResource,
    
}
