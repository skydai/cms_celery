# -*- coding: utf-8 -*-
import sys
import uuid

from flask import request
from flask.ext.restplus import Namespace
from flask.ext.restplus import Resource

from api.parsers import *

sys.path.append('./..')
from cms_celery.k8s_tasks import *

k8s = Namespace('k8s', description="Celery K8s Operation")


@k8s.route('/create_service', strict_slashes=False)
class K8s(Resource):

    @k8s.doc(description='Create K8s Service')
    @k8s.expect(install_k8s_service_params)
    def post(self):

        params = request.json

        tenant_name = 'argon' + str(str(uuid.uuid4())[0:4])
        params['tenant_name'] = str(tenant_name)
#        K8sService.create_service(params)
        res = k8s_create_service.delay(params)
        return {"task_id": str(res.id), "tenant_name": str(tenant_name)}

#
# @k8s.route('/delete_service/<String:tenant_name>', strict_slashes=False)
# class K8s(Resource):
#
#     @k8s.doc(description='Create Instances And Service')
#     def delete(self):
#         K8sService.create_service(params)