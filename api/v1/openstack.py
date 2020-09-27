# -*- coding: utf-8 -*-
import sys

from celery import chain
from flask import request
from flask.ext.restplus import Namespace
from flask.ext.restplus import Resource

from api.parsers import *

sys.path.append('./..')
from cms_celery.openstack_tasks import *

ostack = Namespace('openstack', description="Celery Openstack Operation")


@ostack.route('/verify_user', strict_slashes=False)
class Openstack(Resource):

    @ostack.doc(description='Verify Login User')
    @ostack.expect(openstack_user_params)
    def post(self):
        params = request.json
        msg, status = OpenstackService.verify_openstack_user(params=params)

        return {"status": msg}, status


@ostack.route('/create_instance', strict_slashes=False)
class Openstack(Resource):

    @ostack.doc(description='Create Instances And Service')
    @ostack.expect(create_instance_params)
    def post(self):
        params = request.json
        # OpenstackService.create_instance(params=params)

        res = chain(o_create_instance.s(params), o_call_back.s(), o_send_email.s())()
        return {"task_ids": get_taskID(res)}


@ostack.route('/install_manager', strict_slashes=False)
class Openstack(Resource):

    @ostack.doc(description='Install Manager')
    @ostack.expect(install_manager_service_params)
    def post(self):
        params = request.json
        res = chain(o_install_manager.s(params), o_call_back.s(), o_send_email.s())()
        return {"task_ids": get_taskID(res)}


@ostack.route('/install_service', strict_slashes=False)
class Openstack(Resource):

    @ostack.doc(description='Install Service')
    @ostack.expect(install_service_params)
    def post(self):
        params = request.json
        res = chain(o_install_service.s(params), o_call_back.s(), o_send_email.s())()
        return {"task_ids": get_taskID(res)}


@ostack.route('/create_instance_to_service', strict_slashes=False)
class Openstack(Resource):

    @ostack.doc(description='Create Instances TO Service')
    @ostack.expect(create_instance_to_service_params)
    def post(self):
        params = request.json
        res = chain(o_create_instance.s(params), o_install_manager.s(), o_install_service.s(), o_call_back.s(), o_send_email.s())()
        return {"task_ids": get_taskID(res)}


@ostack.route('/create_instance_to_manager', strict_slashes=False)
class Openstack(Resource):

    @ostack.doc(description='Create Instances TO Manager')
    @ostack.expect(create_instance_to_service_params)
    def post(self):
        params = request.json
        res = chain(o_create_instance.s(params), o_install_manager.s(), o_call_back.s(),  o_send_email.s())()
        return {"task_ids": get_taskID(res)}


@ostack.route('/install_manager_to_serive', strict_slashes=False)
class Openstack(Resource):

    @ostack.doc(description='Install Manager TO Service')
    @ostack.expect(install_manager_service_params)
    def post(self):
        params = request.json
        res = chain(o_install_manager.s(params), o_install_service.s(), o_call_back.s(), o_send_email.s())()
        return {"task_ids": get_taskID(res)}


@ostack.route('/delete_instance')
class Openstack(Resource):

    @ostack.doc(description='delete instance by name')
    @ostack.expect(delete_instance_params)
    def post(self):
        params = request.json
        # OpenstackService.delete_instance(params=params)
        res = chain(o_delete_instance.s(params), o_send_email.s())()
        return {"task_ids": get_taskID(res)}