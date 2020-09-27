# -*- coding: utf-8 -*-
import sys

from flask.ext.restplus import Namespace
from flask.ext.restplus import Resource

sys.path.append('./..')
from celery.result import AsyncResult
tasks = Namespace('tasks', description="Celery Tasks Operation")


@tasks.route('/<string:task_ids>')
class Tasks(Resource):

    @tasks.doc(description='Get Task Info', strict_slashes=False)
    def get(self, task_ids):

        task_ids = [x for x in task_ids.split(',')]
        is_finished = True
        for task_id in task_ids:
            if str(AsyncResult(task_id).status) == 'FAILURE':
                return {"status": "FAILURE"}
            elif str(AsyncResult(task_id).status) == 'PENDING':
                is_finished = False

        if is_finished:
            return {"status": "SUCCESS"}
        else:
            return {"status": "PENDING"}
