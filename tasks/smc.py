import traceback

import requests
import sentry_sdk
from bson import ObjectId
from pydash import get

from config import Config
from helper.contracts.crypto_currencies import CryptoCurrenciesHelpers
from lib import TaskStatus, ContractInsertType
from lib.logger import debug
from models import NFTContractsModel, UsersTemplatesModel
from worker import worker
from connect import redis_cluster


@worker.task(name='worker.create_domain', rate_limit='1000/s')
def create_domain(user: str, subdomain: str, contract_id: str, template_id: str):
    debug(f'Worker: Create domain ----- Contract ID: {contract_id}')

    _create_domain_status_key = f'smc:template_id:{template_id}:create_domain:status'
    try:
        # _status_code, _resp = iapi_services.check_campaign_subdomain_valid(subdomain=subdomain)
        # if _status_code != 200:
        #     return False, "Can't verify subdomain!"
        #
        # if not _resp["data"]["result"]:
        #     return False, "Subdomain not valid!"
        _payload = {
            "domain": subdomain,
            "campaign_id": contract_id
        }

        _resp = requests.post(f'{Config.INZ_IAPI_BASE_URL}/domain', json=_payload, verify=False, timeout=30)
        _code_create_new_domain = _resp.status_code
        _resp_create_new_domain = _resp.json()

        debug(f'Call IAPI service create domain {subdomain}: {_resp.status_code}  {_resp.text}')

        if _code_create_new_domain != 200:
            redis_cluster.set(_create_domain_status_key, TaskStatus.FAIL)
            debug(f"Contract ID: {contract_id} ----- Create subdomain failed!")
            debug(f'Code {_code_create_new_domain}')
            return 'FAIL'

        if _resp_create_new_domain['data'] == {}:
            redis_cluster.set(_create_domain_status_key, TaskStatus.FAIL)
            debug(f"Contract ID: {contract_id} ----- Create subdomain failed!")
            debug(f'Code {_resp_create_new_domain["error_code"]}')
            debug(f'Msg {_resp_create_new_domain["msg"]}')
            return 'FAIL'

        UsersTemplatesModel.update_one(
            filter={
                "user_id": ObjectId(user),
                "template_id": ObjectId(template_id),
            },
            obj={
                'website_domain': subdomain,
                'updated_by': 'inz-nft-api:tasks:create_domain'
            }
        )

        redis_cluster.set(_create_domain_status_key, TaskStatus.DONE)
        debug(f"Create subdomain successfully! {_resp_create_new_domain['data']['result']}")
        return 'DONE'

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        redis_cluster.set(_create_domain_status_key, TaskStatus.FAIL)
        debug(f"Contract ID: {contract_id} ----- Create subdomain failed with exception!")
        return 'FAIL'


@worker.task(name="worker.create_contract_smc", rate_limit="1000/s")
def create_contract_smc(contract_id, *args, **kwargs):
    debug(f'Worker: Create SMC ----- Contract ID: {contract_id}')

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
            debug(f"Contract ID: {contract_id} ----- Create smc failed!")
            debug(f'Code {res.status_code}')
            return 'FAIL'

        debug(f"Contract ID: {contract_id} ----- Create smc success!")
        return 'DONE'

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        redis_cluster.set(_create_smc_status_key, TaskStatus.FAIL)
        debug(f"Contract ID: {contract_id} ----- Create contract failed with exception!")
        return 'FAIL'


@worker.task(name="worker.insert_new_contract", rate_limit="1000/s")
def insert_new_contract(data: dict, user: str, standard: str):
    _template_id = get(data, 'template_id')
    debug(f'Worker: Insert New SMC ----- User ID: {user} ----- Template ID: {_template_id}')
    try:
        # Fixed currency for demo
        _currency_address = CryptoCurrenciesHelpers.get_address_by_symbol(
            symbol=get(data, 'currency'),
            chain=get(data, 'chain')
        )

        del data['template_id']

        _contract_inserted = NFTContractsModel.insert_one({
            **data,
            'standard': standard,
            'type': ContractInsertType.CREATE,
            'deploy_address': '',
            'currency_address': _currency_address.lower(),
            'is_deleted': False,
            'deleted_time': None,
            'deleted_by': '',
            'created_by': 'inz-nft-api:tasks:insert_new_contract',
            'updated_by': ''
        })

        # TODO: Limit contracts user can create
        _user_template = UsersTemplatesModel.find_one(
            filter={
                'user_id': ObjectId(user),
                'template_id': ObjectId(_template_id),
            }
        )
        _user_contracts = get(_user_template, 'contracts', [])
        _user_contracts.append(get(_contract_inserted, '_id'))

        UsersTemplatesModel.update_one(
            filter={'_id': ObjectId(get(_user_template, '_id'))},
            obj={
                'contracts': _user_contracts,
                'updated_by': 'inz-nft-api:tasks:insert_new_contract'
            }
        )

        debug(f"User ID: {user} ----- Template ID: {_template_id} ----- Insert user contract success")
        return 'DONE'

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        debug(f"User ID: {user} ----- Template ID: {_template_id} ----- Insert user contract failed with exception!")
        return 'FAIL'
