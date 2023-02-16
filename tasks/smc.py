from pydash import get

from worker import worker


@worker.task(name='worker.task_create_smc', rate_limit='1000/s')
def task_create_smc(data):
    _standard = get(data, 'standard')
    _chain = get(data, 'chain')
    _user = get(data, 'user')
    _template = get(data, 'template')
    _user = get(data, 'user')
