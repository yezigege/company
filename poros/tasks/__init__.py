import datetime
import json
import time

from celery import Celery
from celery._state import get_current_task
from celery.app.log import TaskFormatter
from celery.signals import task_postrun, task_prerun, \
    after_setup_task_logger
from celery.utils.log import get_task_logger
from util.date_util import DateUtil
from util.profile import Profiler


d, p = {}, {}
celery_app = Celery(__name__)

logger = get_task_logger(__name__)

@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(TaskFormatter('%(message)s'))


@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **extras):
    d[task_id] = int(time.time() * 1000)
    pr = Profiler.get_profiler(task.name)
    if pr:
        p[task_id] = pr


@task_postrun.connect
def after_task_run(sender=None, headers=None, body=None, **kwargs):
    task_id = kwargs.get('task_id')
    task_args = kwargs.get('args', [])
    task_kwargs = kwargs.get('kwargs', {})
    retval = kwargs.get('retval')
    state = kwargs.get('state')
    task = get_current_task()
    end_ms = int(time.time() * 1000)
    begin_ms = d.pop(task_id) if task_id in d else end_ms

    try:
        pr = p.pop(task_id, None)
        if pr:
            pr.disable()
            Profiler.end(task.name, pr)
    except Exception:
        pass

    logger.info(json.dumps(dict(
        task_id=task_id,
        task_name=task.name,
        args=task_args,
        kwargs=task_kwargs,
        retval=retval,
        state=state,
        begin_time=DateUtil.datetime_to_str(x=datetime.datetime.fromtimestamp(begin_ms/1000)),
        cost=end_ms - begin_ms,
        queue_name=task.request.delivery_info['routing_key'],
    ), ensure_ascii=False))
