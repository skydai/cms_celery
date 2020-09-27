from flask_restplus import reqparse
from flask_restplus.fields import *

from api import api
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

###########################
# Delete Instance
###########################
delete_instance_params = api.model('Delete Instance Params', {
    'o_username': String(required=True),
    'o_password': String(required=True),
    'instance_name':  String(required=True),
})


###########################
# Instance Manager Service
###########################
create_instance_to_service_params = api.model('Instance And Service Create Params', {
    'name': String(required=True),
    'o_image_id': String(required=True, default='320495d1-4d5f-440a-a290-f0fdd8cd8f7e'),
    'o_flavor_id': String(required=True, default='ebb9a776-7f96-4761-b345-373df63b7876'),
    'description': String,
    'instance_num': Integer(required=True, default=1),
    'volume_num_every_instance': Integer(required=True, default=1),
    'o_username': String(required=True),
    'o_password': String(required=True),
    'boot_volume_type': String(required=False, default='ssd'),
    'boot_volume_size': String(required=True),
    'tdh_version': String(required=True),
    'service_list': String(required=True),
    'email': String(required=False, default='youzhi.su@transwarp.io'),
    'pre_hostname': String(required=False, default=''),
    'manager_version': String(required=True, default='6.0'),
})

instance_service_create_args = reqparse.RequestParser()
instance_service_create_args.add_argument('create_instance_to_service_params', type=create_instance_to_service_params, location='json')


###########################
# Openstack User
###########################
openstack_user_params = api.model('Openstack User Params', {
    'o_username': String(required=True),
    'o_password': String(required=True),
})

openstack_user_args = reqparse.RequestParser()
openstack_user_args.add_argument('openstack_user_params', type=openstack_user_params, location='json')


###########################
# Instance
###########################
create_instance_params = api.model('Instance Create Params', {
    'name': String(required=True),
    'o_image_id': String(required=True, default='320495d1-4d5f-440a-a290-f0fdd8cd8f7e'),
    'o_flavor_id': String(required=True, default='ebb9a776-7f96-4761-b345-373df63b7876'),
    'description': String,
    'instance_num': Integer(required=True, default=1),
    'volume_num_every_instance': Integer(required=True, default=1),
    'o_username': String(required=True),
    'o_password': String(required=True),
    'boot_volume_type': String(required=False, default='ssd'),
    'boot_volume_size': String(required=True),
    'email': String(required=False, default='youzhi.su@transwarp.io'),
    'pre_hostname': String(required=False, default=''),

})

instance_create_args = reqparse.RequestParser()
instance_create_args.add_argument('create_instance_params', type=create_instance_params, location='json')


###########################
# Manager
###########################

instance_list_params = api.model('Instance List Params', {
    'username': String(required=True, default='root'),
    'password': String(required=True, default='transwarp123'),
    'float_ip': String(required=True),
    'inner_ip': String(required=True),
    'name':  String(required=False),
})

install_manager_service_params = api.model('Manager And Service Install Params', {
    'pre_hostname': String(required=False),
    'tdh_version': String(required=True, default='transwarp-5.1'),
    'nodes': List(Nested(instance_list_params)),
    'date': String(required=False, default='latest'),
    'service_list': String(required=False, default='INCEPTOR'),
    'email': String(required=False, default='youzhi.su@transwarp.io'),
    'manager_version': String(required=True, default='6.0'),
})

manager_service_install_args = reqparse.RequestParser()
manager_service_install_args.add_argument('install_manager_service_params', type=install_manager_service_params, location='json')

#################################
# Service
#################################

install_service_params = api.model('Service Install Params', {
    'tdh_version': String(required=True, default='transwarp-5.1'),
    'nodes': List(Nested(instance_list_params)),
    'service_list': String(required=False, default='INCEPTOR'),
    'email': String(required=False, default='youzhi.su@transwarp.io'),
})

service_install_args = reqparse.RequestParser()
service_install_args.add_argument('install_service_params', type=install_service_params, location='json')


###########################
# k8s
###########################
k8s_image_url_params = api.model('K8s Image Url Param', {
    'hdfs_image': String(required=False, default=''),
    'httpfs_image': String(required=False, default=''),
    'zookeeper_image': String(required=False, default=''),
    'yarn_image': String(required=False, default=''),
    'inceptor_image': String(required=False, default=''),
    'hbase_image': String(required=False, default=''),
    'search_image': String(required=False, default=''),
    'txsql_image': String(required=False, default=''),
    'sophon_server_image': String(required=False, default=''),
})

install_k8s_service_params = api.model('Install K8s Service', {
    'service_tag': String(required=True, default='transwarp-5.2'),
    'vcpus': String(required=True, default='1'),
    'ram': String(required=True, default='1'),
    'service_name': String(required=False, default='INCEPTOR'),
    'images': Nested(k8s_image_url_params, required=False),
    'enable_kerberos': Boolean(required=False, default=False),
})

install_k8s_service_args = reqparse.RequestParser()
install_k8s_service_args.add_argument('install_k8s_service_params', type=install_k8s_service_params, location='json')

task_info_params = api.model('Task Info Params', {
    'task_id': String(requird=True, default=''),
})


