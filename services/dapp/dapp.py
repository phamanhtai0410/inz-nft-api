# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class INZDappServices:
    def __init__(self, client):
        self.client = client

    def is_user_template_exist(self, params):
        return self.client.get('/user/template/is_exist', params=params)
