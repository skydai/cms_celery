from __future__ import absolute_import, unicode_literals

from celery import chain

from cms_celery.openstack_tasks import *

if __name__ == '__main__':

    params ={'service_list': 'INCEPTOR', 'nodes': [{'name': 'lisong6e121', 'hostname': 't036f01', 'inner_ip': '10.0.10.45', 'user': 'root', 'float_ip': '172.16.132.116', 'password': 'transwarp123'}, {'name': 'lisong6e122', 'hostname': 't036f02', 'inner_ip': '10.0.10.34', 'user': 'root', 'float_ip': '172.16.132.128', 'password': 'transwarp123'}, {'name': 'lisong6e123', 'hostname': 't036f03', 'inner_ip': '10.0.10.53', 'user': 'root', 'float_ip': '172.16.132.148', 'password': 'transwarp123'}], 'email': 'lisong.qiu@transwarp.io', 'tdh_version': 'transwarp-4.9.1-final'}

    OpenstackService.install_service(params=params)

    # chain(o_create_instance.s(params), o_install_manager.s(), o_install_service.s(), o_send_email.s())()
