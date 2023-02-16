from bson import ObjectId
from pydash import get
from models import UsersContractsModel


class UsersContractsHelpers:

    @classmethod
    def is_contract_owner(cls, user, contract_id):
        _user_contract = UsersContractsModel.find_one(filter={
            '_id': ObjectId(contract_id)
        })

        if _user_contract is None:
            return False

        if str(get(_user_contract, 'user_id')) != str(user):
            return False

        return True
