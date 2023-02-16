# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.smc.create_contract import SMCCreateContractResource
from resources.smc.update_non_released_contract import SMCUpdateNonReleasedContractResource

smc_resources = {
    '/create': SMCCreateContractResource,
    '/update/non_released': SMCUpdateNonReleasedContractResource,
}
