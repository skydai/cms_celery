# -*- coding: utf-8 -*-
import os
from datetime import timedelta
from kombu import Exchange, Queue

from celery.schedules import crontab

#BROKER_URL = os.getenv('BROKER_URL', 'redis://127.0.0.1:6379/')
# CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'db+mysql://root:transwarp@127.0.0.1:3306/cms_celery')

BROKER_URL = os.getenv('BROKER_URL', 'redis://172.16.1.161:30908/')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'db+mysql://root:transwarp@172.16.130.96:30637/cms_celery')

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = (
    'cms_celery.openstack_tasks',
    'cms_celery.k8s_tasks',
)

CELERYD_LOG_LEVEL="DEBUG"

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ["json"]
CELERYD_PREFETCH_MULTIPLIER = 5
CELERYD_CONCURRENCY = 20
CELERYD_FORCE_EXECV = True    # 防止死锁

# # schedules
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=10),       # 每 30 秒执行一次
#          'args': (5, 8)                           # 任务函数参数
#     },
#     'multiply-at-some-time': {
#         'task': 'celery_app.task2.multiply',
#         'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
#         'args': (3, 7)                            # 任务函数参数
#     }
# }


CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('for_task_A', Exchange('for_task_A'), routing_key='for_task_A'),
    Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERYD_MAX_TASKS_PER_CHILD = 200
CELERY_MAX_TASKS_PER_CHILD = 200