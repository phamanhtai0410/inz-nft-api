import traceback

import requests
import sentry_sdk

from config import Config
from lib import TaskStatus
from lib.logger import debug
from worker import worker
from connect import redis_cluster


@worker.task(name='worker.create_domain', rate_limit='1000/s')
def create_domain(iapi_services, subdomain: str, contract_id: str):
    debug('Worker: Create domain ----- Contract ID: ', contract_id)

    _create_domain_status_key = f'smc:_id:{contract_id}:create_domain:status'
    try:
        # _status_code, _resp = iapi_services.check_campaign_subdomain_valid(subdomain=subdomain)
        # if _status_code != 200:
        #     return False, "Can't verify subdomain!"
        #
        # if not _resp["data"]["result"]:
        #     return False, "Subdomain not valid!"

        _code_create_new_domain, _resp_create_new_domain = iapi_services.create_new_subdomain(
            subdomain=subdomain,
            contract_id=contract_id
        )

        if _code_create_new_domain != 200:
            redis_cluster.set(_create_domain_status_key, TaskStatus.FAIL)
            debug('-' * 20)
            debug(f"Contract ID: {contract_id} ----- Create subdomain failed!")
            debug('Code', _code_create_new_domain)
            debug('-' * 20)

        if _resp_create_new_domain['data'] == {}:
            redis_cluster.set(_create_domain_status_key, TaskStatus.FAIL)
            debug('-' * 20)
            debug(f"Contract ID: {contract_id} ----- Create subdomain failed!")
            debug('Code', _resp_create_new_domain['error_code'])
            debug('Msg', _resp_create_new_domain['msg'])
            debug('-' * 20)

        redis_cluster.set(_create_domain_status_key, TaskStatus.DONE)
        debug('-' * 20)
        debug("Create subdomain successfully!")
        debug(_resp_create_new_domain['data']['result'])
        debug('-' * 20)

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        redis_cluster.set(_create_domain_status_key, TaskStatus.FAIL)
        debug('-' * 20)
        debug(f"Contract ID: {contract_id} ----- Create subdomain failed with exception!")
        debug('-' * 20)


@worker.task(name="worker.create_contract_smc", rate_limit="1000/s")
def create_contract_smc(contract_id, *args, **kwargs):
    debug('Worker: Create SMC ----- Contract ID: ', contract_id)

    _create_smc_status_key = f'smc:_id:{contract_id}:create_smc:status'
    try:
        _payload = {
            "_id": contract_id
        }

        res = requests.post(
            f"{Config.WALLET_IAPI}/deploy/contract",
            json=_payload,
            timeout=20
        )

        if res.status_code != 200:
            redis_cluster.set(_create_smc_status_key, TaskStatus.FAIL)
            debug('-' * 20)
            debug(f"Contract ID: {contract_id} ----- Create smc failed!")
            debug('Code', res.status_code)
            debug('-' * 20)

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        redis_cluster.set(_create_smc_status_key, TaskStatus.FAIL)
        debug('-' * 20)
        debug(f"Contract ID: {contract_id} ----- Create contract failed with exception!")
        debug('-' * 20)
