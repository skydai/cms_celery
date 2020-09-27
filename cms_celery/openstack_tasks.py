from __future__ import absolute_import, unicode_literals

import time

# import sys
# sys.path.append('./..')
from celery import Task

from cms_celery.callbacktasks import CreateInstanceCallbackTask
from openstack.openstack import OpenstackService
from .celery import app


@app.task(base=CreateInstanceCallbackTask)
def o_create_instance(params):
    return OpenstackService.create_instance(params=params)


@app.task(base=CreateInstanceCallbackTask)
def o_install_manager(params):
    return OpenstackService.install_manager(params=params)


@app.task(base=CreateInstanceCallbackTask)
def o_delete_instance(params):
    return OpenstackService.delete_instance(params=params)


@app.task(base=CreateInstanceCallbackTask)
def o_install_service(params):
    return OpenstackService.install_service(params=params)


@app.task(base=CreateInstanceCallbackTask)
def o_send_email(params):
    return OpenstackService.send_email(params=params)


@app.task(base=CreateInstanceCallbackTask)
def o_call_back(params):
    return OpenstackService.call_back(params=params)


@app.task(base=CreateInstanceCallbackTask)
def o_add(x, y):
    time.sleep(200)
    #raise Exception('xxxx')
    return x + y


@app.task
def o_mul(x, y):
    time.sleep(10)
    return x * y


@app.task
def o_div(x, y):
    return x / y


@app.task
def o_xsum(numbers):
    time.sleep(10)
    return sum(numbers)


@app.task
def get_taskID(res):
    result = []
    while res is not None:
        result.append(res.id)
        res = res.parent

    result.reverse()
    return ','.join(result)
