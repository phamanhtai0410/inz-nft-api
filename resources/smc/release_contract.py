# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas import SMCReleaseContractRequestSchema, SMCReleaseContractResponseSchema
from services import SMCServices


class SMCReleaseContractResource(Resource):

    @security.http(
        form_data=SMCReleaseContractRequestSchema(),
        response=SMCReleaseContractResponseSchema(),
        login_required=True
    )
    def post(self, form_data, login_info):
        _id, _domain, _create_domain_status, _create_smc_status = SMCServices.release_contract(
            user=str(get(login_info, 'user._id')),
            data=form_data
        )

        return {
            '_id': _id,
            'domain': _domain,
            'create_domain_status': _create_domain_status,
            'create_smc_status': _create_smc_status
        }
