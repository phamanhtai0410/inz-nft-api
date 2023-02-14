from bson import ObjectId
from pydash import get
from models import NFTContractsModel


class SMCServices:

    @classmethod
    def create_contract(cls, user: str, data: dict):
        # TODO: check template id of user

        _user_contract = NFTContractsModel.insert_one({
            'user_id': ObjectId(user),
            'contract': '',
            'name': get(data, 'name'),
            'symbol': get(data, 'symbol'),
            'total_supply': get(data, 'total_supply'),
            'royalty': get(data, 'royalty'),
            'chain': get(data, 'chain'),
            'standard': get(data, 'standard'),
            'image': get(data, 'image'),
            'created_by': 'inz-nft-api:services:AdminServices:create_contract',
            'updated_by': '',
        })
        _id = str(get(_user_contract, '_id', ''))

        # TODO: task create smc

        return {
            'id': _id
        }
