import web3
import pydash as py_

from config import Config
from lib import dt_utcnow


class SignatureHelper:

    @staticmethod
    def generate_signature(data):
        '''
        '''

        _chain_id = py_.get(data, 'chain_id')
        _user_address = py_.get(data, 'user_address')
        _contract_address = py_.get(data, 'contract_address')
        _nft_address = py_.get(data, 'nft_address')
        _discount = py_.get(data, 'discount', 0)
        _is_whitelist = py_.get(data, 'is_whitelist', False)
        _nft_type = py_.get(data, 'nft_type')
        _amount = py_.get(data, 'amount')
        _deadline = int(dt_utcnow().timestamp() + Config.SIGNATURE_EXPIRE_TIME)

        _web3 = web3.Web3()

        _encode = _web3.codec.encode_abi(
            [
                'uint256', # chain_id
                'address', # user_address
                'address', # contract creator
                'address', # collection address
                'uint256', # discount
                'bool', # is whitelist
                'uint8', # nft_type
                'uint256', # amount
                'uint256' # deadline
            ],
            [
                _chain_id,
                _user_address,
                _contract_address,
                _nft_address,
                _discount,
                _is_whitelist,
                _nft_type,
                _amount,
                _deadline
            ]
        )

        _digest = web3.Web3.solidityKeccak(['bytes'], [f'0x{_encode.hex()}'])
        _signed_message = _web3.eth.account.signHash(
            _digest,
            private_key=Config.AUTH_PRIVATE_KEY
        )

        return _signed_message.signature.hex()

