from bson import ObjectId
from pydash import get

from connect import redis_cluster
from models import UsersTemplatesModel


class UserTemplateHelpers:
    @classmethod
    def is_use_template_with_contract(cls, user: str, contract_address: str, user_template_id: str):
        # _key = ''
        # redis_cluster.get()
        # TODO: Get contract with template user have add from redis
        return True
