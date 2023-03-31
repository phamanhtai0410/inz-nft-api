# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from bson import ObjectId
from flask_restful import Resource
from pydash import get

from connect import security
from schemas import SMCCreateContractRequestSchema, SMCCreateContractResponseSchema
from services import SMCServices


class SMCCreateContractResource(Resource):

    @security.http(
        form_data=SMCCreateContractRequestSchema(),
        response=SMCCreateContractResponseSchema(),
        login_required=True
    )
    def post(self, form_data, login_info):
        _name, _is_released = SMCServices.create_contract(
            user=str(get(login_info, 'user._id')),
            data={
                'contract': '',
                'is_released': False,
                **form_data
            }
        )

        return {
            'name': _name,
            'is_released': _is_released
        }
