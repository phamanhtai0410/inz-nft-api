import uuid
import pydash as py_

from helper.signature import SignatureHelper
from models import SignatureLogModel


class SMCSignatureService:

    @staticmethod
    def create_signature(form_data):
        # NOTE: does not have rule about discount and whitelist yet
        _discount = int(0)
        _is_whitelist = False

        _sign_data = {
            **form_data,
            'user_address': py_.get(form_data, 'user_address').lower(),
            'contract_address': py_.get(form_data, 'contract_address').lower(),
            'nft_address': py_.get(form_data, 'nft_address').lower(),
            'discount': _discount,
            'is_whitelist': _is_whitelist
        }

        _signature, _deadline = SignatureHelper.generate_signature(data=_sign_data)

        _log_id = str(uuid.uuid4())

        SignatureLogModel.insert_one({
            **_sign_data,
            'log_id': _log_id,
            'signature': _signature,
            'deadline': _deadline,
            'created_by': 'inz-nft-api:SMCSignatureService:SM:create_signature'
        }, worker=True)

        return {
            'data': {
                **_sign_data,
                'callback': _log_id
            },
            'signature': _signature,
            'deadline': _deadline
        }
