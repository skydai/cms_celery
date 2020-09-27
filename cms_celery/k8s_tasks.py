from __future__ import absolute_import, unicode_literals

import time

# import sys
# sys.path.append('./..')
from celery import Task

from cms_celery.callbacktasks import CreateInstanceCallbackTask
from k8s.k8s import K8sService
from .celery import app


@app.task(base=CreateInstanceCallbackTask)
def k8s_create_service(params):
    return K8sService.create_service(params=params)


@app.task(base=CreateInstanceCallbackTask)
def k_add(x, y):
    time.sleep(10)
    return x + y


@app.task
def k_mul(x, y):
    time.sleep(10)
    return x * y

@app.task
def K_div(x, y):
    return x/y


@app.task
def k_xsum(numbers):
    time.sleep(10)
    return sum(numbers)