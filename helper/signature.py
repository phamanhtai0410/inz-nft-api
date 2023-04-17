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

        return _signed_message.signature.hex(), _deadline

    @staticmethod
    def generate_buy_nft_signature(data):
        '''
        '''

        _web3 = web3.Web3()

        _chain_id = py_.get(data, 'chain_id')
        _order_id = py_.get(data, 'order_id')
        _to_address = _web3.toChecksumAddress(py_.get(data, 'to_address'))
        _nft_address = _web3.toChecksumAddress(py_.get(data, 'nft_address'))
        _currency_address = _web3.toChecksumAddress(py_.get(data, 'currency_address'))
        _nft_id = py_.get(data, 'token_id')
        _price = py_.get(data, 'price')
        _owner_address = _web3.toChecksumAddress(py_.get(data, 'owner_address'))
        _currency_decimal = py_.get(data, 'currency_decimal')
        _standard = py_.get(data, 'standard')

        _price = _web3.toWei(str(_price), py_.get(Config.BLOCKCHAIN_DECIMALS, str(_currency_decimal), 'ether'))


        _allAmounts = [_price]

        _from_to = [_owner_address, _to_address]
        _nft_and_token = [_nft_address, _currency_address]
        _id_and_amount = [_nft_id, _standard]
        #FIXME: current is only have seller does not have any other
        _additional_token_receivers = []

        #FIXME: current is only owner get all amount
        _all_amounts = [_price]

        _deadline = int(dt_utcnow().timestamp() + Config.SIGNATURE_BUY_NFT_EXPIRE_TIME)

        _type_list = [
            "uint256",
            "uint256",
            "address[2]",
            "address[2]",
            "uint256[2]",
            "address[]",
            "uint256[]",
            "uint256",
        ]

        _value_list =  [
                _chain_id,
                _order_id,
                _from_to,
                _nft_and_token,
                _id_and_amount,
                _additional_token_receivers,
                _all_amounts,
                _deadline
            ]

        _message_hash = web3.Web3.solidityKeccak(_type_list, _value_list).hex()
        _msg = web3.Web3.solidityKeccak(
            ["string", "bytes32"],
            ["\x19Ethereum Signed Message:\n32", _message_hash],
        ).hex()
        _signed_message = _web3.eth.account.signHash(
            _msg,
            private_key=Config.AUTH_PRIVATE_KEY
        )
        return {
            'signature': _signed_message.signature.hex(), 
            'data': {
                'order_id': _order_id,
                'from_to': _from_to,
                'nft_and_token': _nft_and_token,
                'id_and_amount': _id_and_amount,
                'additional_token_receivers': _additional_token_receivers,
                'all_amounts': _all_amounts,
            },
            'deadline': _deadline
        }