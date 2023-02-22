import traceback

import requests
import sentry_sdk

from config import Config
from lib.logger import debug
from worker import worker


@worker.task(name='worker.create_domain', rate_limit='1000/s')
def create_domain(iapi_services, subdomain: str, contract_id: str):
    try:
        _status_code, _resp = iapi_services.check_campaign_subdomain_valid(subdomain=subdomain)
        if _status_code != 200:
            return False, "Can't verify subdomain!"

        if not _resp["data"]["result"]:
            return False, "Subdomain not valid!"

        _code_create_new_domain, _resp_create_new_domain = iapi_services.create_new_subdomain(
            subdomain=subdomain,
            contract_id=contract_id
        )

        if _code_create_new_domain != 200:
            return False, f"Create subdomain failed! {_code_create_new_domain}"

        if _resp_create_new_domain['data'] == {}:
            return False, \
                   f"Create subdomain failed! {_resp_create_new_domain['error_code']} {_resp_create_new_domain['msg']}"

        return _resp_create_new_domain['data']['result'], "Create subdomain successfully!"

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return False, "Create subdomain false!"


@worker.task(name="worker.create_contract_smc", rate_limit="1000/s")
def create_contract_smc(contract_id, *args, **kwargs):
    """
        Call to Wallet-IAPI to create new contract
    """
    debug('worker - contract id : ', contract_id)
    _payload = {
        "_id": contract_id
    }

    debug("worker : ", _payload)
    resp = requests.post(
        f"{Config.WALLET_IAPI}/deploy/contract",
        json=_payload,
        timeout=10
    )

    debug("wallet iapi response: ", resp.json())
    return "success"

