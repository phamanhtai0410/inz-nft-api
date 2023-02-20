from pydash import get
from models import CryptoCurrenciesModel


class CryptoCurrenciesHelpers:

    @classmethod
    def get_address_by_symbol(cls, symbol, chain):
        _crypto_currencies = CryptoCurrenciesModel.find_one(filter={
            'symbol': symbol,
            'chain': chain
        })

        return get(_crypto_currencies, 'contract_address', '')
