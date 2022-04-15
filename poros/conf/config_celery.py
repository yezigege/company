"""celery配置"""
from celery.schedules import crontab

from conf.settings import CELERY_REDIS_SETTINGS

timezone = 'Asia/Shanghai'  # 时区配置
task_serializer = 'json'  # 指定序列化方式
accept_content = ['json']  # 指定任务接受的序列化类型
task_ignore_result = False   # 不存储任务状态，默认 False
result_serializer = 'json'  # 指定结果序列化方式
task_time_limit = 600  # 单个任务的运行时间不超过此值，否则会被SIGKILL信号杀死

# Broker 任务队列中间人
broker_url = 'redis://:%s@%s:%s/%s' % (CELERY_REDIS_SETTINGS['password'], CELERY_REDIS_SETTINGS['host'],
                                       CELERY_REDIS_SETTINGS['port'], CELERY_REDIS_SETTINGS['db'])

redis_max_connections = 5

task_create_missing_queues = True  # 某个程序中出现的队列，在broker中不存在，则立刻创建它
worker_max_tasks_per_child = 1000  # 每个worker执行了多少任务就会死掉
task_default_queue = 'default'

# 设定定时调用
# https://www.celerycn.io/yong-hu-zhi-nan/ding-qi-ren-wu-periodic-tasks
# beat_schedule = {
#     'celery_task_test': {
#         'task': 'tasks.ceshi.celery_task_test',
#         'schedule': 5,
#     },
# }

# 限定指定任务到指定的服务器处理
# queue:  high_task:高优先级任务  long_time_task:长耗时任务(结果不是特别重要的任务)  default:默认优先级任务
# https://www.celerycn.io/yong-hu-zhi-nan/lu-you-ren-wu-routing-tasks
task_routes = {
    'tasks.ceshi.celery_task_test': {'queue': 'ceshi'},
}
imports = (
    'tasks.ceshi',
)
