# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

import sentry_sdk

from lib.logger import debug


class IAPIServices:
    def __init__(self, client):
        self.client = client

    def check_campaign_subdomain_valid(self, subdomain, campaign_id=None):
        try:
            _payload = {
                "domain": subdomain
            }

            if campaign_id:
                _payload["campaign_id"] = campaign_id

            resp = self.client.post('/domain/check', json=_payload, verify=False, timeout=5)
            debug(f'Call IAPI service check domain {subdomain}: {resp.status_code}  {resp.text}')

            return resp.status_code, resp.json()
        except:
            sentry_sdk.capture_exception()
            traceback.print_exc()
            return 400, {}

    """
        Function: Call IAPI service to create new subdomain
        @params: 
        @return: True or False
    """

    def create_new_subdomain(self, subdomain, campaign_id):
        try:
            _payload = {
                "domain": subdomain,
                "campaign_id": campaign_id
            }

            resp = self.client.post('/domain', json=_payload, verify=False, timeout=5)

            debug(f'Call IAPI service create domain {subdomain}: {resp.status_code}  {resp.text}')

            return resp.status_code, resp.json()
        except:
            sentry_sdk.capture_exception()
            traceback.print_exc()
            return 400, {}
