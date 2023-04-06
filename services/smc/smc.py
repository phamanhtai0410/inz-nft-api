from datetime import timezone, datetime
from bson import ObjectId
from pydash import get
from slugify import slugify
from config import Config
from helper.contracts.crypto_currencies import CryptoCurrenciesHelpers
from helper.user.user_template import UserTemplateHelpers
from lib import ClientAPI, BadRequest, dt_utcnow, TokenStandard, TaskStatus, ContractInsertType
from lib.logger import debug
from models import NFTContractsModel, UsersTemplatesModel
from services.dapp import INZDappServices
from services.iapi import IAPIServices
from tasks import create_domain, create_contract_smc, insert_new_contract, send_task_import_contract
from connect import redis_cluster

_inz_dapp_client = ClientAPI(host=Config.INZ_DAPP_BASE_URL)
_inz_dapp_services = INZDappServices(client=_inz_dapp_client)

_iapi_client = ClientAPI(host=Config.INZ_IAPI_BASE_URL)
_iapi_services = IAPIServices(client=_iapi_client)


class SMCServices:

    @classmethod
    def create_contract(cls, user: str, data: dict):
        _result = _inz_dapp_services.is_user_template_exist(params={
            'user_template': get(data, 'user_template_id')
        })
        if _result.status_code == 400:
            raise BadRequest(msg='Invalid params.', errors=get(_result.json(), 'errors'))

        _list_nft = get(data, 'nft_list', [])
        _standard = TokenStandard.ERC721

        # TODO: check token standard
        # if _list_nft:
        #     _standard = TokenStandard.ERC1155

        # if get(data, 'is_box'):
        #     _standard = TokenStandard.ERC721
        #     _sum_percent = sum([nft['percent'] if 'percent' in nft else 0 for nft in _list_nft])
        #     if _sum_percent != 100:
        #         raise BadRequest(msg='Invalid Nft List.', errors=['Total percent not valid!'])
        # else:
        #     _sum_supply = sum([nft['supply'] for nft in _list_nft])
        #     _sum_raise = sum([nft['supply'] * nft['price'] for nft in _list_nft])
        #
        #     if _sum_supply != get(data, 'total_supply'):
        #         raise BadRequest(msg='Invalid Nft List.', errors=['Total supply not valid!'])
        #
        #     if _sum_raise != data["total_raise"]:
        #         raise BadRequest(msg='Invalid Nft List', errors=['Total raise not valid!'])

        # NOTE: Check later when release
        # _check_domain_status_code, _check_subdomain_resp = _iapi_services.check_campaign_subdomain_valid(
        #     get(data, 'website_domain'))

        # if _check_domain_status_code != 200:
        #     raise BadRequest(f"Submitted subdomain error: {_check_subdomain_resp['msg']}")
        #
        # if _check_domain_status_code == 200 and not _check_subdomain_resp['data']['result']:
        #     raise BadRequest(msg='Invalid params.', errors=['Subdomain already exist!'])

        debug("*** Contract dict : ", data)
        debug("*** Contract dict - nft list: ", _list_nft)

        data["nft_list"] = [{**x, 'index_type': idx + 1} for idx, x in enumerate(_list_nft)]

        debug("Contract dict have index_type 2: ", data)

        # insert nft_contracts, users_contracts
        # Fixed currency for demo
        _currency_address = CryptoCurrenciesHelpers.get_address_by_symbol(
            symbol=get(data, 'currency'),
            chain=get(data, 'chain')
        )

        _user_template_id = get(data, 'user_template_id')
        del data['user_template_id']

        _contract_inserted = NFTContractsModel.insert_one({
            **data,
            'standard': _standard,
            'type': ContractInsertType.CREATE,
            'deploy_address': '',
            'currency_address': _currency_address.lower(),
            'user_id': ObjectId(user),
            'is_deleted': False,
            'deleted_time': None,
            'deleted_by': '',
            'created_by': 'inz-nft-api:tasks:insert_new_contract',
            'updated_by': ''
        })
        insert_new_contract.delay(
            user_template_id=str(_user_template_id),
            user=user,
            contract_id=str(get(_contract_inserted, '_id'))
        )

        return _contract_inserted

    @classmethod
    def update_non_released_contract(cls, user, data, contract_id):
        _contract = NFTContractsModel.find_one(filter={'_id': ObjectId(contract_id)})

        if _contract is None:
            raise BadRequest(msg='Invalid params.', errors=['Contract does not exist.'])
        # if 'nft_list' in data:
        _list_nft = get(data, 'nft_list', [])
        _standard = TokenStandard.ERC721

        # if _list_nft:
        #     _standard = TokenStandard.ERC1155

        if _contract["is_deleted"]:
            raise BadRequest(msg="This contract's already been deleted!")

        # if data["is_box"]:
        #     _standard = TokenStandard.ERC721
        #     _sum_percent = sum([nft['percent'] for nft in _list_nft])
        #     if _sum_percent != 100:
        #         raise BadRequest(msg='Invalid Nft List.', errors=['Total percent not valid!'])
        # else:
        #     _sum_supply = sum([nft['supply'] for nft in _list_nft])
        #     _sum_raise = sum([nft['supply'] * nft['price'] for nft in _list_nft])
        #
        #     if _sum_supply != data['total_supply']:
        #         raise BadRequest(msg='Invalid Nft List.', errors=['Total supply not valid!'])
        #     if _sum_raise != data["total_raise"]:
        #         raise BadRequest(msg='Invalid Nft List.', errors=['Total raise not valid!'])

        if str(_contract['user_id']) != user:
            raise BadRequest(msg="Not have permission to update this contract!")

        if _contract['is_released']:
            raise BadRequest(msg="This contract's already released!")

        if 'nft_list' in data:
            data["nft_list"] = [{**x, 'index_type': get(x, 'index_type', idx + 1)} for idx, x in
                                enumerate(data['nft_list'])]

        _currency_address = CryptoCurrenciesHelpers.get_address_by_symbol(
            symbol=get(data, 'currency'),
            chain=get(data, 'chain')
        )

        NFTContractsModel.update_one(
            filter={
                "_id": ObjectId(contract_id)
            },
            obj={
                **data,
                'currency_address': _currency_address,
                'standard': _standard,
                'updated_by': 'inz-nft-api:services:SMCServices:update_non_released_contract'
            }
        )

        return contract_id, True

    @classmethod
    def update_released_contract(cls, user, data, contract_id):
        _contract = NFTContractsModel.find_one(filter={'_id': ObjectId(contract_id)})
        if _contract is None:
            raise BadRequest(msg='Invalid params.', errors=['Contract does not exist.'])

        if str(_contract['user_id']) != user:
            raise BadRequest(msg="Not have permission to update this contract!")

        if _contract["is_deleted"]:
            raise BadRequest(msg="This contract's already been deleted!")

        if not _contract['is_released']:
            raise BadRequest(msg="This contract is not released!")

        NFTContractsModel.update_one(
            filter={
                "_id": ObjectId(contract_id)
            },
            obj={
                **data,
                'updated_by': 'inz-nft-api:services:SMCServices:update_released_contract'
            }
        )

        return contract_id, True

    @classmethod
    def import_contract(cls, user, data, contract_address):
        _user_template_id = get(data, 'user_template_id')
        _is_exist, _contract = UserTemplateHelpers.is_use_template_with_contract(
            user=user,
            contract_address=contract_address,
            user_template_id=_user_template_id
        )
        if _is_exist:
            raise BadRequest(msg="Contract is already used with this template.")

        debug("*** Contract import : ", data)

        if _contract is None:
            _contract_inserted = NFTContractsModel.insert_one({
                **data,
                'currency_address': '',
                'is_released': False,
                'type': ContractInsertType.IMPORT,
                'user_id': ObjectId(user),
                'is_deleted': False,
                'deleted_time': None,
                'deleted_by': '',
                'created_by': 'inz-nft-api:services:SMCServices:import_contract',
                'updated_by': ''
            })
            return _contract_inserted
        # send_task_import_contract.delay({'chain': get(data, 'chain'), 'address': get(data, 'address')})

        return _contract

    @classmethod
    def release_contract(cls, user, data):
        _contract_id = str(get(data, 'contract_id'))
        _website_domain = slugify(get(data, 'website_domain', ''))
        _user_template_id = str(get(data, 'user_template_id'))
        _contract = NFTContractsModel.find_one(filter={'_id': ObjectId(_contract_id)})
        _user_template = UsersTemplatesModel.find_one(filter={
            '_id': ObjectId(_user_template_id),
        })
        _user_contracts = get(_user_template, 'contracts', [])

        if _contract is None:
            raise BadRequest(msg='Invalid params.', errors=['Collection does not exist.'])

        if ObjectId(_contract_id) not in _user_contracts:
            raise BadRequest(msg="Not have permissions to release this contract!")

        if get(_contract, 'is_deleted'):
            raise BadRequest(msg="This collection's already been deleted!")

        # if True => imported contract else created contract
        _is_import = get(_contract, 'contract', '') != ''

        _create_domain_status = TaskStatus.DONE
        if _website_domain not in get(_user_template, 'website_domain', []):
            _create_domain_status_key = f'smc:user_template_id:{_user_template_id}:create_domain:{_website_domain}:status'
            _create_domain_status = redis_cluster.get(_create_domain_status_key)
            if not _create_domain_status or _create_domain_status == TaskStatus.FAIL:
                _check_domain_status_code, _check_subdomain_resp = _iapi_services.check_campaign_subdomain_valid(
                    _website_domain)

                if _check_domain_status_code != 200:
                    raise BadRequest(f"Submitted subdomain error: {_check_subdomain_resp['msg']}")

                if _check_domain_status_code == 200 and not _check_subdomain_resp['data']['result']:
                    raise BadRequest(msg='Invalid params.', errors=['Subdomain already exist!'])

                create_domain.delay(
                    user=user,
                    subdomain=_website_domain,
                    contract_id=_contract_id,
                    user_template_id=_user_template_id
                )
                redis_cluster.set(_create_domain_status_key, TaskStatus.PROCESSING)
                _create_domain_status = TaskStatus.PROCESSING

        _create_smc_status = TaskStatus.DONE
        if not _is_import:
            _create_smc_status_key = f'smc:_id:{_contract_id}:create_smc:status'
            _create_smc_status = redis_cluster.get(_create_smc_status_key)
            if not _create_smc_status or _create_smc_status == TaskStatus.FAIL:
                for _key, _value in _contract.items():
                    if isinstance(_value, ObjectId):
                        _contract[_key] = str(_value)
                    if isinstance(_value, datetime):
                        _contract[_key] = _value.replace(tzinfo=timezone.utc).timestamp()

                debug(f'_contract_dict after encode: {_contract} ----- type: {type(_contract)}')

                create_contract_smc.delay(
                    contract_id=_contract_id
                )
                redis_cluster.set(_create_smc_status_key, TaskStatus.PROCESSING)
                _create_smc_status = TaskStatus.PROCESSING

        return _contract_id, _website_domain, _create_domain_status, _create_smc_status

    @classmethod
    def delete_contract(cls, user, contract_id):
        _contract = NFTContractsModel.find_one(filter={'_id': ObjectId(contract_id)})

        if _contract is None:
            raise BadRequest(msg='Invalid params.', errors=['Contract does not exist.'])

        if _contract['user_id'] != ObjectId(user):
            raise BadRequest(msg="Not have permissions to release this contract!")

        if _contract["is_deleted"]:
            raise BadRequest(msg="This contract's already been deleted!")

        NFTContractsModel.update_one(
            filter={
                "_id": ObjectId(contract_id)
            },
            obj={
                'is_deleted': True,
                'deleted_time': dt_utcnow(),
                'updated_time': dt_utcnow(),
                'updated_by': 'inz-nft-api:services:SMCServices:delete_contract'
            }
        )
        return True

    @classmethod
    def get_contracts(
            cls,
            user: str,
            page: int = 1,
            page_size: int = 10
    ):
        _filter = {'user_id': ObjectId(user)}

        _offset = page > 0 and (page - 1) * page_size or 0

        _pipeline = [
            {
                '$match': _filter
            },
            {
                '$lookup': {
                    'from': 'templates',
                    'localField': 'template_id',
                    'foreignField': '_id',
                    'as': 'template',
                }
            },
            {
                '$unwind': '$template'
            },
            {
                '$lookup': {
                    'from': 'template_categories',
                    'localField': 'template.category_id',
                    'foreignField': '_id',
                    'as': 'category',
                }
            },
            {
                '$unwind': '$category'
            },
            {
                '$skip': _offset
            },
            {
                '$limit': page_size
            }
        ]

        _items = NFTContractsModel.col.aggregate(pipeline=_pipeline)

        _items = list(_items)

        print(_items)

        _num_of_page = (len(_items) / page_size)
        if (len(_items) % page_size) > 0:
            _num_of_page = _num_of_page + 1

        return {
            'items': _items,
            'page': page,
            'page_size': page_size,
            'num_of_page': _num_of_page
        }
