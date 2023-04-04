import web3
import pydash as py_

from models import NFTsModel


class NFTsServices:

    @classmethod
    def get_nfts(
            cls,
            page,
            page_size: int,
            chain: str = None,
            contracts: str = None,
            sort_field: str = None,
            sort_type: str = None
    ):
        _filter = {'on_market': True}
        _func_sort = None
        _sort = None

        if chain is not None:
            _filter['chain'] = chain

        _web3 = web3.Web3()
        _contracts = [x.lower() for x in contracts if _web3.isAddress(x) ]
        if not _contracts:
            return {}

        if _contracts:
            _filter['contract'] = {
                '$in': _contracts
            }

        if sort_field and sort_type:
            _func_sort = lambda x: py_.get(x, sort_field)
            _sort = 1 if sort_type == 'asc' else -1

        # if sort_price is not None:
        #     _sort = {'price': sort_price.lower() == 'asc' and 1 or -1}

        # _offset = page > 0 and (page - 1) * page_size or 0

        # _pipeline = [
        #     {
        #         '$match': _filter
        #     },
        #     {
        #         '$skip': _offset
        #     },
        #     {
        #         '$limit': page_size
        #     }
        # ]

        # if _sort:
        #     _pipeline.append({'$sort': _sort})

        # _items = NFTsModel.col.aggregate(pipeline=_pipeline)

        # _items = list(_items)

        # print(_items)

        # _num_of_page = (len(_items) / page_size)
        # if (len(_items) % page_size) > 0:
        #     _num_of_page = _num_of_page + 1

        # return {
        #     'items': _items,
        #     'page': page,
        #     'page_size': page_size,
        #     'num_of_page': _num_of_page
        # }

        _results = NFTsModel.page(
            filter=_filter,
            page=page,
            page_size=page_size,
            sort=_sort,
            func_sort=_func_sort
        )

        return _results
