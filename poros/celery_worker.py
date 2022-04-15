"""
celery -A your_application.celery worker -Q app_task1  # 指定worker执行哪个队列中的任务
celery -A proj beat -s /home/celery/var/run/celerybeat-schedule
"""
from celery import platforms

from apps import create_app
from tasks import celery_app  # 不可缺少
from log_config import logger_celery

logger_celery.info("msg celery starting .........")
platforms.C_FORCE_ROOT = True
app = create_app()
app.app_context().push()
