from bson import ObjectId
from pydash import get

from connect import redis_cluster
from models import UsersTemplatesModel, NFTContractsModel


class UserTemplateHelpers:
    @classmethod
    def is_use_template_with_contract(cls, user: str, contract_address: str, user_template_id: str):
        # _key = ''
        # redis_cluster.get()
        # TODO: Get contract with template user have add from redis
        _contract = NFTContractsModel.find_one({"contract": contract_address})
        if _contract is None:
            return False, None

        _user_template = UsersTemplatesModel.find_one({
            '_id': ObjectId(user_template_id),
            'contracts': {
                '$elemMatch': {
                    '$eq': get(_contract, '_id')
                }
            }
        })
        if _user_template is None:
            return False, _contract
        return True, _contract
