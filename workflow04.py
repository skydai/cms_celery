from __future__ import absolute_import, unicode_literals

from celery import chain

from cms_celery.openstack_tasks import *

if __name__ == '__main__':

    params = {'service_list': 'INCEPTOR', 'nodes': [{'username': 'root', 'name': 'qimengf0991', 'hostname': 't3fcc01', 'inner_ip': '10.0.12.13', 'float_ip': '172.16.132.205', 'password': 'transwarp123'}, {'username': 'root', 'name': 'qimengf0992', 'hostname': 't3fcc02', 'inner_ip': '10.0.12.6', 'float_ip': '172.16.132.203', 'password': 'transwarp123'}, {'username': 'root', 'name': 'qimengf0993', 'hostname': 't3fcc03', 'inner_ip': '10.0.12.3', 'float_ip': '172.16.132.202', 'password': 'transwarp123'}], 'email': 'qimeng.wang@transwarp.io', 'tdh_version': 'transwarp-5.1.3-final'}

    #OpenstackService.send_email(params=params)


    # OpenstackService.install_manager(params=params)

    # chain(o_add.s(1, 2), o_send_email.si(params))()

    # chain(o_create_instance.s(params), o_install_manager.s(), o_install_service.s(), o_send_email.s())()
