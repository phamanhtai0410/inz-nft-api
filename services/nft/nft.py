from models import NFTsModel


class NFTsServices:

    @staticmethod
    def get_nfts(
            page: int = 1,
            page_size: int = 10,
            chain: str = None,
            contract: str = None,
            sort_price: str = None,
    ):
        _filter = {'on_sale': True}
        _sort = {}

        if chain is not None:
            _filter['chain'] = chain
        if contract is not None:
            _filter['contract'] = contract.lower()

        if sort_price is not None:
            _sort = {'price': sort_price.lower() == 'asc' and 1 or -1}

        _offset = page > 0 and (page - 1) * page_size or 0

        _pipeline = [
            {
                '$match': _filter
            },
            {
                '$skip': _offset
            },
            {
                '$limit': page_size
            }
        ]

        if _sort:
            _pipeline.append({'$sort': _sort})

        _items = NFTsModel.col.aggregate(pipeline=_pipeline)

        _items = list(_items)

        # print(_items)

        _num_of_page = (len(_items) / page_size)
        if (len(_items) % page_size) > 0:
            _num_of_page = _num_of_page + 1

        return {
            'items': _items,
            'page': page,
            'page_size': page_size,
            'num_of_page': _num_of_page
        }
