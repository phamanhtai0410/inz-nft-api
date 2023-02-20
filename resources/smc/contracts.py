# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas import ContractsRequestSchema, ContractsResponseSchema
from services import SMCServices


class ContractsResource(Resource):

    @security.http(
        params=ContractsRequestSchema(),
        response=ContractsResponseSchema(),
        login_required=True
    )
    def get(self, params, login_info):

        _page = get(params, 'page', default=1)
        _page_size = get(params, 'page_size', default=10)

        _response = SMCServices.get_contracts(
            user=str(get(login_info, 'user._id')),
            page=_page,
            page_size=_page_size
        )

        return _response
