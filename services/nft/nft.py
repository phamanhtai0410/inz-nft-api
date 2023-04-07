import web3
import pydash as py_
import bson

from models import NFTContractsModel, NFTsModel
from lib import dt_utcnow

class NFTsServices:

    @staticmethod
    def mapping_nft_detail(nft_items):
        _nft_contracts = {}

        def get_nft_detail(item, contract, type):
            _buy_deadline = py_.get(item, 'buy_deadline').timestamp() if py_.get(item, 'buy_deadline') else 0
            _now = dt_utcnow().timestamp()
            _on_market = True if _buy_deadline > _now else False
            return {
                **item,
                'image_url': py_.get(_nft_contracts[contract], f'nft_list.{type - 1}.image_url'),
                'name': py_.get(_nft_contracts[contract], f'nft_list.{type - 1}.name'),
                # NOTE: if nft does not have previous price on sale will get default price
                'price': py_.get(item, 'price') if py_.get(item, 'price') != None and _on_market else py_.get(_nft_contracts[contract], f'nft_list.{type - 1}.price'),
                'on_market': _on_market,

            }

        _items = []

        for _item in nft_items:
            _contract = py_.get(_item, 'contract').lower()
            _type = py_.get(_item, 'type')
            if _contract in _nft_contracts:
                _item = get_nft_detail(_item, _contract, _type)
                _items.append(_item)
                continue
            
            # NOTE: cache later
            _nft_contract = NFTContractsModel.find_one({
                'contract': _contract
            })

            if not _nft_contract:
                continue

            py_.set_(_nft_contracts, _contract, _nft_contract)

            _item = get_nft_detail(_item, _contract, _type)

            _items.append(_item)

        return _items


    @classmethod
    def get_nfts(
            cls,
            page,
            page_size: int,
            chain: str = None,
            contracts: str = None,
            sort_field: str = None,
            sort_type: str = None,
            user_id: str = None,
            filter = {}
    ):
        _filter = {
            **filter
        }
        _func_sort = None
        _sort = None

        if chain is not None:
            _filter['chain'] = chain

        if contracts:
            _web3 = web3.Web3()
            _contracts = [x.lower() for x in contracts if _web3.isAddress(x) ]
            if not _contracts:
                return {}

            if _contracts:
                _filter['contract'] = {
                    '$in': _contracts
                }

        if user_id and bson.objectid.ObjectId.is_valid(user_id):
            _filter['user'] = bson.objectid.ObjectId(user_id)

        if sort_field and sort_type:
            _func_sort = lambda x: py_.get(x, sort_field)
            _sort = 1 if sort_type == 'asc' else -1

        _results = NFTsModel.page(
            filter=_filter,
            page=page,
            page_size=page_size,
            sort=_sort,
            func_sort=_func_sort
        )

        _items = NFTsServices.mapping_nft_detail(py_.get(_results, 'items'))

        py_.set_(_results, 'items', _items)
        
        return _results

    @staticmethod
    def get_marketplace_by_contracts(params):
        _page = py_.get(params, 'page', default=1)
        _page_size = py_.get(params, 'page_size', default=10)
        _chain = py_.get(params, 'chain', default=None)
        _sort_field = py_.get(params, 'sort_field', default=None)
        _sort_type = py_.get(params, 'sort_type', default=None)
        _contracts = py_.get(params, 'contracts', default=None)

        if not _contracts:
            return {}

        # NOTE: if buy_deadline existed and valid with time -> on_market will mark at true
        _result = NFTsServices.get_nfts(
            filter={
                'buy_deadline': {
                    '$gt': dt_utcnow()
                }
            },
            page=_page,
            page_size=_page_size,
            chain=_chain,
            contracts=_contracts,
            sort_field=_sort_field,
            sort_type=_sort_type,
        )

        return _result

    @staticmethod
    def get_user_nfts(user_id, params):
        _page = py_.get(params, 'page')
        _page_size = py_.get(params, 'page_size')
        _sort_field = py_.get(params, 'sort_field')
        _sort_type = py_.get(params, 'sort_type')
        _chain = py_.get(params, 'chain', None)
        _contracts = py_.get(params, 'contracts', None)

        _result = NFTsServices.get_nfts(
            page=_page,
            page_size=_page_size,
            chain=_chain,
            contracts=_contracts,
            sort_field=_sort_field,
            sort_type=_sort_type,
            user_id=user_id
        )

        return _result