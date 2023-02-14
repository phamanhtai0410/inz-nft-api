from worker import worker


@worker.task(name='worker.task_create_smc', rate_limit='1000/s')
def task_create_smc(standard, chain):
    pass
