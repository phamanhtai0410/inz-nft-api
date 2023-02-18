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
from schemas import SMCImportContractRequestSchema, SMCImportContractResponseSchema
from services import SMCServices


class SMCImportContractResource(Resource):

    @security.http(
        form_data=SMCImportContractRequestSchema(),
        response=SMCImportContractResponseSchema(),
        login_required=True
    )
    def post(self, form_data, login_info):
        _import_data = form_data
        _contract_address = get(form_data, 'contract')
        _import_data['template_id'] = ObjectId(form_data['template_id'])

        _id, _result = SMCServices.import_contract(
            user=str(get(login_info, 'user._id')),
            data=_import_data,
            contract_address=_contract_address.lower()
        )

        return {
            '_id': _id,
            'result': _result
        }
