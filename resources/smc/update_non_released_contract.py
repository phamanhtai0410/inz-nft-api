# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas import SMCUpdateNonReleasedContractRequestSchema, SMCUpdateNonReleasedContractResponseSchema
from services import SMCServices


class SMCUpdateNonReleasedContractResource(Resource):

    @security.http(
        form_data=SMCUpdateNonReleasedContractRequestSchema(),
        response=SMCUpdateNonReleasedContractResponseSchema(),
        login_required=True
    )
    def put(self, form_data, login_info):
        _edit_data = form_data
        _contract_id = get(form_data, '_id')
        del _edit_data['_id']

        _id, _result = SMCServices.update_non_released_contract(
            user=str(get(login_info, 'user._id')),
            data=_edit_data,
            contract_id=_contract_id
        )

        return {
            '_id': _id,
            'result': _result
        }
