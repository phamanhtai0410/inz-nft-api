# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.smc.create_contract import SMCCreateContractResource
from resources.smc.update_non_released_contract import SMCUpdateNonReleasedContractResource
from resources.smc.update_released_contract import SMCUpdateReleasedContractResource

smc_resources = {
    '/create': SMCCreateContractResource,
    '/update/non_released': SMCUpdateNonReleasedContractResource,
    '/update/released': SMCUpdateReleasedContractResource,
}
