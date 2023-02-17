from datetime import timezone, datetime

from bson import ObjectId
from pydash import get

from config import Config
from enums.contract import ContractInsertType
from lib import ClientAPI, BadRequest, dt_utcnow
from lib.logger import debug
from models import NFTContractsModel
from services.dapp import INZDappServices
from services.iapi import IAPIServices
from tasks import create_domain, create_contract_smc

_inz_dapp_client = ClientAPI(host=Config.INZ_DAPP_BASE_URL)
_inz_dapp_services = INZDappServices(client=_inz_dapp_client)

_iapi_client = ClientAPI(host=Config.INZ_IAPI_BASE_URL)
_iapi_services = IAPIServices(client=_iapi_client)


class SMCServices:

    @classmethod
    def create_contract(cls, user: str, data: dict):
        _result = _inz_dapp_services.is_user_template_exist(params={
            'template': get(data, 'template_id'),
            'user': user
        })
        if _result.status_code == 400:
            raise BadRequest(msg='Invalid params.', errors=get(_result.json(), 'errors'))

        _list_nft = get(data, 'nft_list')

        if get(data, 'is_box'):
            _sum_percent = sum([nft['percent'] if 'percent' in nft else 0 for nft in _list_nft])
            if _sum_percent != 100:
                raise BadRequest(msg='Invalid Nft List.', errors=['Total percent not valid!'])
        else:
            _sum_supply = sum([nft['supply'] for nft in _list_nft])
            _sum_raise = sum([nft['supply'] * nft['price'] for nft in _list_nft])

            if _sum_supply != get(data, 'total_supply'):
                raise BadRequest(msg='Invalid Nft List.', errors=['Total supply not valid!'])

            if _sum_raise != data["total_raise"]:
                raise BadRequest(msg='Invalid Nft List', errors=['Total raise not valid!'])

        # Check if subdomain
        _check_domain_status_code, _check_subdomain_resp = _iapi_services.check_campaign_subdomain_valid(
            get(data, 'website_domain'))

        if _check_domain_status_code != 200:
            raise BadRequest(f"Submitted subdomain error: {_check_subdomain_resp['msg']}")

        if _check_domain_status_code == 200 and not _check_subdomain_resp['data']['result']:
            raise BadRequest(msg='Invalid params.', errors=['Subdomain already exist!'])

        debug("*** Contract dict : ", data)
        debug("*** Contract dict - nft list: ", _list_nft)

        data["nft_list"] = [{**x, 'index_type': idx + 1} for idx, x in enumerate(_list_nft)]

        debug("Contract dict have index_type 2: ", data)

        NFTContractsModel.insert_one({
            'user_id': ObjectId(user),
            **data,
            'type': ContractInsertType.CREATE,
            'is_deleted': False,
            'deleted_time': None,
            'deleted_by': '',
            'created_by': 'inz-nft-api:services:SMCServices:create_contract',
            'updated_by': ''
        })

        return get(data, 'name'), get(data, 'is_released')

    @classmethod
    def update_non_released_contract(cls, user, data, contract_id):
        _contract = NFTContractsModel.find_one(filter={'_id': ObjectId(contract_id)})

        if _contract is None:
            raise BadRequest(msg='Invalid params.', errors=['Contract does not exist.'])
        # if 'nft_list' in data:
        _list_nft = data['nft_list']

        if _contract["is_deleted"]:
            raise BadRequest(msg="This contract's already been deleted!")

        if data["is_box"]:
            _sum_percent = sum([nft['percent'] for nft in _list_nft])
            if _sum_percent != 100:
                raise BadRequest(msg='Invalid Nft List.', errors=['Total percent not valid!'])
        else:
            _sum_supply = sum([nft['supply'] for nft in _list_nft])
            _sum_raise = sum([nft['supply'] * nft['price'] for nft in _list_nft])

            if _sum_supply != data['total_supply']:
                raise BadRequest(msg='Invalid Nft List.', errors=['Total supply not valid!'])
            if _sum_raise != data["total_raise"]:
                raise BadRequest(msg='Invalid Nft List.', errors=['Total raise not valid!'])

        if str(_contract['user_id']) != user:
            raise BadRequest(msg="Not have permission to update this contract!")

        if _contract['is_released']:
            raise BadRequest(msg="This contract's already released!")

        if 'nft_list' in data:
            data["nft_list"] = [{**x, 'index_type': get(x, 'index_type', idx + 1)} for idx, x in
                                enumerate(data['nft_list'])]

        NFTContractsModel.update_one(
            filter={
                "_id": ObjectId(contract_id)
            },
            obj={
                **data,
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
        _contract = NFTContractsModel.find_one(filter={
            'contract': contract_address,
            'chain': get(data, 'chain'),
            'user_id': ObjectId(user)
        })
        if _contract is not None:
            raise BadRequest(msg='Invalid params.', errors=['Contract is exist.'])

        # Check if subdomain
        _check_domain_status_code, _check_subdomain_resp = _iapi_services.check_campaign_subdomain_valid(
            get(data, 'website_domain'))

        if _check_domain_status_code != 200:
            raise BadRequest(f"Submitted subdomain error: {_check_subdomain_resp['msg']}")

        if _check_domain_status_code == 200 and not _check_subdomain_resp['data']['result']:
            raise BadRequest(msg='Invalid params.', errors=['Subdomain already exist!'])

        debug("*** Contract import : ", data)
        _contract_id = NFTContractsModel.insert_one({
            'user_id': ObjectId(user),
            **data,
            'max_allocation': None,
            'nft_list': [],
            'is_released': True,
            'type': ContractInsertType.IMPORT,
            'is_deleted': False,
            'deleted_time': None,
            'deleted_by': '',
            'created_by': 'inz-nft-api:services:SMCServices:import_contract',
            'updated_by': ''
        })

        return _contract_id, True

    @classmethod
    def release_contract(cls, user, contract_id):
        _contract = NFTContractsModel.find_one(filter={'_id': ObjectId(contract_id)})

        if _contract is None:
            raise BadRequest(msg='Invalid params.', errors=['Contract does not exist.'])

        if _contract['is_released']:
            raise BadRequest(msg="This contract's already released!")

        if _contract['user_id'] != ObjectId(user):
            raise BadRequest(msg="Not have permissions to release this contract!")

        if _contract["is_deleted"]:
            raise BadRequest(msg="This contract's already been deleted!")

        #    Create subdomain for contract
        #       @params: subdomain need to be created
        #       @return: result of creation: True or False and created subdomain
        _creation_result, _msg = create_domain(
            iapi_services=_iapi_services,
            contract_id=contract_id,
            subdomain=_contract["website_domain"]
        )
        print("*** Subdomain Creation Result : ", _creation_result)

        if _creation_result:
            #       Call to CampaignFactory to deploy new contract contract
            #       params: infors of contracts
            #       return: created contract's address
            print('_contract_dict : ', _contract, type(_contract))
            print('_contract_id : ', contract_id, type(contract_id))

            for _key, _value in _contract.items():
                if isinstance(_value, ObjectId):
                    _contract[_key] = str(_value)
                if isinstance(_value, datetime):
                    _contract[_key] = _value.replace(tzinfo=timezone.utc).timestamp()

            print('_contract_dict after encode: ', _contract, type(_contract))

            create_contract_smc.delay(
                contract_dict=dict(_contract),
                contract_id=contract_id
            )

        return contract_id, _creation_result, _msg

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
                "is_deleted": True,
                "deleted_time": dt_utcnow()
            }
        )
        return True



