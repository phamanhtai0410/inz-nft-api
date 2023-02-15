from bson import ObjectId
from pydash import get

from config import Config
from lib import ClientAPI, BadRequest
from lib.logger import debug
from models import NFTContractsModel
from services.dapp import INZDappServices
from services.iapi import IAPIServices

_inz_dapp_client = ClientAPI(host=Config.INZ_DAPP_BASE_URL)
_inz_dapp_services = INZDappServices(client=_inz_dapp_client)

_iapi_client = ClientAPI(host=Config.IAPI_BASE_URL)
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

        if get(data, 'random_nft'):
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
        # _check_domain_status_code, _check_subdomain_resp = _iapi_services.check_campaign_subdomain_valid(
        #     get(data, 'website_domain'))
        #
        # if _check_domain_status_code != 200:
        #     raise BadRequest(f"Submitted subdomain error: {_check_subdomain_resp['msg']}")
        #
        # if _check_domain_status_code == 200 and not _check_subdomain_resp['data']['result']:
        #     raise BadRequest(msg='Invalid params.', errors=['Subdomain already exist!'])

        debug("*** Contract dict : ", data)
        debug("*** Contract dict - nft list: ", _list_nft)

        data["nft_list"] = [{**x, 'index_type': idx + 1} for idx, x in enumerate(_list_nft)]

        debug("Contract dict have index_type 2: ", data)

        NFTContractsModel.insert_one({
            **data,
            'created_by': 'inz-nft-api:services:SMCServices:create_contract',
            'updated_by': ''
        })

        return get(data, 'name'), get(data, 'is_released')

