import traceback

import requests
import sentry_sdk

from config import Config
from lib import ClientAPI
from services import IAPIServices
from worker import worker


_iapi_client = ClientAPI(host=Config.INZ_IAPI_BASE_URL)
_iapi_services = IAPIServices(client=_iapi_client)


@worker.task(name='worker.create_domain', rate_limit='1000/s')
def create_domain(subdomain: str, contract_id: str):
    try:
        _status_code, _resp = _iapi_services.check_campaign_subdomain_valid(subdomain=subdomain)
        if _status_code != 200:
            return "Can't verify subdomain!"

        if not _resp["data"]["result"]:
            return "Subdomain not valid!"

        _code_create_new_domain, _resp_create_new_domain = _iapi_services.create_new_subdomain(
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
        return False


@worker.task(name="worker.create_campaign_smc", rate_limit="1000/s")
def create_contract_smc(_campaign_dict, _contract_id, *args, **kwargs):
    """
        Call to Wallet-IAPI to create new campaign contract
    """
    print('worker - campaign id : ', _contract_id)
    _payload = {
        "_id": _contract_id,
        "start_time": _campaign_dict["start_time"],
        "end_time": _campaign_dict["end_time"],
        "symbol": _campaign_dict["symbol"],
        "market_address": Config.INZ_MARKET_ADDRESS,
        "factory_address": Config.INZ_CAMPAIGN_FACTORY_ADDRESS,
        "token_address": Config.INZ_COIN_TOKEN_ADDRESS,
        "is_fixed_token": _campaign_dict["is_fixed_token"] if _campaign_dict["is_fixed_token"] else False,
        "name": _campaign_dict["name"]
    }

    print("worker : ", _payload)
    resp = requests.post(
        f"{Config.WALLET_IAPI}/deploy/campaign",
        json=_payload,
        verify=False,
        timeout=10
    )
    return "success"

