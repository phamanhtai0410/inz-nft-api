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
        _contract_id = get(form_data, 'contract_id')
        _id, _result, _msg = SMCServices.release_contract(
            user=str(get(login_info, 'user._id')),
            contract_id=_contract_id
        )

        return {
            "_id": _id,
            "result": _result,
            "messages": _msg
        }

