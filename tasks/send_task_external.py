import traceback
import sentry_sdk
from bson import json_util
from pydash import get
from config import Config
from lib.logger import debug
from worker import worker


@worker.task(name='worker.send_task_import_contract', rate_limit='1000/s')
def send_task_import_contract(data):
    debug(f"Worker: Send task import contract ----- Contract address: {get(data, 'address')} | Chain: {get(data, 'chain')}")
    try:
        _task_name = get(Config.TASKS_NAME, 'IMPORT_CONTRACT')

        if not _task_name:
            sentry_sdk.capture_message(f'FAIL - not config handle for: IMPORT_CONTRACT')
            return 'FAIL'

        worker.send_task(_task_name, (json_util.dumps(data)))
        return 'DONE'
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return 'FAIL'
