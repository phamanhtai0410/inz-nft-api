# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas import SMCDeleteContractRequestSchema, SMCDeleteContractResponseSchema
from services import SMCServices


class SMCDeleteContractResource(Resource):

    @security.http(
        form_data=SMCDeleteContractRequestSchema(),
        response=SMCDeleteContractResponseSchema(),
        login_required=True
    )
    def post(self, form_data, login_info):
        _contract_id = get(form_data, 'contract_id')
        _id, _result = SMCServices.delete_contract(
            user=str(get(login_info, 'user._id')),
            contract_id=_contract_id
        )

        return {
            "_id": _id,
            "result": _result,
        }

