import web3
import pydash as py_
import bson

from models import NFTContractsModel, NFTsModel


class NFTsServices:

    @staticmethod
    def mapping_nft_image_url(nft_items):
        _nft_contracts = {}

        def set_image_url(item, contract, type):
            py_.set_(item, 'image_url', py_.get(_nft_contracts[contract], f'nft_list.{type - 1}.image_url'))

        for _item in nft_items:
            _contract = py_.get(_item, 'contract').lower()
            _type = py_.get(_item, 'type')
            if _contract in _nft_contracts:
                set_image_url(_item, _contract, _type)
                continue
            
            # NOTE: cache later
            _nft_contract = NFTContractsModel.find_one({
                'contract': _contract
            })

            if not _nft_contract:
                continue

            py_.set_(_nft_contracts, _contract, _nft_contract)

            set_image_url(_item, _contract, _type)

        return nft_items


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

        _items = NFTsServices.mapping_nft_image_url(py_.get(_results, 'items'))

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

        _result = NFTsServices.get_nfts(
            filter={
                'on_market': True
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