# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
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

        _name = get(form_data, 'name')
        _symbol = get(form_data, 'symbol')
        _total_supply = get(form_data, 'total_supply')
        _royalty = get(form_data, 'royalty')
        _chain = get(form_data, 'chain')
        _standard = get(form_data, 'standard')
        _image = get(form_data, 'image')
        _template_id = get(form_data, 'template_id')

        _response = SMCServices.create_contract(
            user=str(get(login_info, 'user._id')),
            data={
                'name': _name,
                'symbol': _symbol,
                'total_supply': int(_total_supply),
                'royalty': float(_royalty),
                'chain': _chain,
                'standard': _standard,
                'image': _image,
                'template_id': _template_id
            }
        )

        return _response
