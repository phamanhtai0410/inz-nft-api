import traceback
import web3
import pydash as py_
import bson
import sentry_sdk
from exceptions.nft_contract import NftContractNotFoundEx, NftIndexTypeNotFoundEx
from exceptions.qr_code import QRCodeNotFoundEx

from models import NFTContractsModel, NFTsModel, QrCodeModel
from worker import worker
import bson.json_util


class QrService:

    @staticmethod
    def generate_metamask_qr(form_data):
        _filter = {}
        for prop in form_data:
            _filter[f'properties.{prop}'] = form_data[prop]

        _qr = QrCodeModel.find_one(_filter)
        if _qr:
            return _qr

        _contract_address = py_.get(form_data, 'contract_address')

        _nft_contract = NFTContractsModel.find_one({
            'contract': _contract_address
        })

        if not _nft_contract:
            raise NftContractNotFoundEx

        _index_type = py_.get(form_data, 'index_type')
        if not py_.get(_nft_contract, f'nft_list.{_index_type - 1}'):
            raise NftIndexTypeNotFoundEx

        _image_url = py_.get(_nft_contract, f'nft_list.{_index_type - 1}.image_url')

        worker.send_task('worker.task_generate_metamask_qr_code', (_image_url, bson.json_util.dumps(form_data)))

        raise QRCodeNotFoundEx

