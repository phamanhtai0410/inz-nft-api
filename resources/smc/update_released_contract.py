# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas import SMCUpdateReleasedContractRequestSchema, SMCUpdateReleasedContractResponseSchema
from services import SMCServices


class SMCUpdateReleasedContractResource(Resource):

    @security.http(
        form_data=SMCUpdateReleasedContractRequestSchema(),
        response=SMCUpdateReleasedContractResponseSchema(),
        login_required=True
    )
    def put(self, form_data, login_info):
        _edit_data = form_data
        _contract_id = get(form_data, '_id')
        del _edit_data['_id']

        _id, _result = SMCServices.update_released_contract(
            user=str(get(login_info, 'user._id')),
            data=_edit_data,
            contract_id=_contract_id
        )

        return {
            '_id': _id,
            'result': _result
        }
