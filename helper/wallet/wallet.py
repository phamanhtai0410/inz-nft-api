from enums.blockchain import Chains
from lib import dt_utcnow
from models import WalletsModel, UsersModel


class WalletsHelpers:

    @classmethod
    def user_of(cls, address: str, with_upsert=False):
        _wallet = UsersModel.find_one(filter={
            'public_address': address
        })

        if not _wallet and with_upsert:
            _user = UsersModel.insert_one({
                'username': 'Unnamed',
                'avatar': '',
                'public_address': address,
                'roles': [],
                'created_time': dt_utcnow(),
                'updated_time': dt_utcnow(),
                'created_by': 'inz-api:helper:wallet_helpers:user_of',
                'updated_by': ''
            })

            WalletsModel.insert_one({
                'public_address': address,
                'user': _user['_id'],
                'active': True,
                'network': Chains.BSC_CHAIN,
                'created_time': dt_utcnow(),
                'updated_time': dt_utcnow(),
                'created_by': 'inz-api:helper:wallet_helpers:user_of',
                'updated_by': ''
            })
            return _user

        return _wallet
