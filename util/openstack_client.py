# coding:utf-8
import logging

import time

from util.openstack_config import OpenstackConfig
from util.openstack_util import OpenstackUtil

logger = logging.getLogger(__name__)
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class OpenstackClient(object):

    @classmethod
    def get_subnet_network(cls, project_id, auth_token):

        network = OpenstackUtil.listNetwork(auth_token=auth_token)
        subnets_list = network['networks']
        if subnets_list == [] or subnets_list == '':
            logger.info("cannot get subnet network by project id and auth_token, project_id: %s" % (str(project_id)))
            raise Exception(
                "cannot get subnet network by project id and auth_token, project_id: %s" % (str(project_id)))

        sub_network_id = sub_network_name = ''
        for tmp_subnet in subnets_list:

            if str(tmp_subnet['name']) == str('ext_flat_public'):
                continue

            if str(tmp_subnet['project_id']) == str(project_id):
                sub_network_id = str(tmp_subnet['id'])
                sub_network_name = str(tmp_subnet['name'])
                break
            else:
                continue

        return sub_network_id, sub_network_name


    @classmethod
    def get_project_name_and_id(cls, auth_token):

        project_list = OpenstackUtil.listProjects(auth_token=auth_token)
        if project_list == [] or project_list == '':
            logger.info("cannot get project id and name")
            raise Exception("cannot get project id and name by auth_token, auth_token: %s" % (str(auth_token)))


        return str(project_list['tenants'][0]['name']), str(project_list['tenants'][0]['id'])

    @classmethod
    def get_auto_token(cls, username, password):

        auth_token = OpenstackUtil.getAuthTokenId(username=username, password=password)

        return auth_token

    @classmethod
    def verify_login_user(cls, username, password):

        return OpenstackUtil.verifyLoginUser(username=username, password=password)

    @classmethod
    def get_auto_token_and_project(cls, project_name, username, password):

        auth_token, project_id = OpenstackUtil.getAuthTokenAndProjectId(project_name=project_name, username=username,
                                                                        password=password)

        return auth_token, project_id

    @classmethod
    def create_boot_volume(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        volume_name = kwargs['boot_volume_name']
        boot_volume_size = kwargs['boot_volume_size']
        image_id = kwargs['o_image_id']
        boot_volume_availabiliity_zone = kwargs['boot_volume_availabiliity_zone']
        boot_volume_type = kwargs['boot_volume_type']

        boot_volume_response = OpenstackUtil.createBootVolumeByImage(auth_token=auth_token, project_id=project_id,
                                                                     volume_name=volume_name,
                                                                     volume_size=boot_volume_size,
                                                                     image_id=image_id,
                                                                     availability_zone=boot_volume_availabiliity_zone,
                                                                     volume_type=boot_volume_type)

        boot_volume_id = str(boot_volume_response['volume']['id'])

        logger.info("create boot volume suc... volume id: %s, volume name: %s" % (boot_volume_id, volume_name))

        if OpenstackClient.check_volume_status(auth_token, project_id, boot_volume_id) == "available":
            return boot_volume_response
        else:
            raise Exception("boot volume status not available. boot_volume_response: %s" % str(boot_volume_response))

    @classmethod
    def create_instance_by_boot_volume(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        boot_volume_size = kwargs['boot_volume_size']
        image_id = kwargs['o_image_id']
        boot_volume_availabiliity_zone = kwargs['boot_volume_availabiliity_zone']
        instance_name = kwargs['instance_name']
        flavor_id = kwargs['o_flavor_id']
        inner_network_id = kwargs['inner_network_id']
        boot_volume_id = kwargs['boot_volume_id']

        if OpenstackClient.check_volume_status(auth_token, project_id, boot_volume_id) == "available":
            instance_response = OpenstackUtil.createInstanceFromVolume(auth_token, project_id,
                                                                       instance_name=instance_name,
                                                                       image_ref_id=image_id,
                                                                       flavor_ref_id=flavor_id,
                                                                       network_id=inner_network_id,
                                                                       volume_id=boot_volume_id,
                                                                       volume_size=boot_volume_size,
                                                                       user_data="",
                                                                       availability_zone=boot_volume_availabiliity_zone)

            instance_id = str(instance_response['server']['id'])

            if OpenstackClient.check_instance_status(auth_token, project_id, instance_id) == "ACTIVE":
                return instance_response
            else:
                raise Exception("create instance from volume failed. instance_response: %s" % (str(instance_response)))

        else:
            raise Exception("create instance by boot volume failed, volume status not available")

    @classmethod
    def create_blank_volume(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        volume_disk_size = kwargs['volume_disk_size']
        volume_availabiliity_zone = kwargs['volume_availabiliity_zone']
        volume_type = kwargs['blank_volume_type']
        volume_name = kwargs['blank_volume_name']

        volume_response = OpenstackUtil.createBlankVolume(auth_token=auth_token, project_id=project_id,
                                                          volume_name=volume_name, volume_size=volume_disk_size,
                                                          availability_zone=volume_availabiliity_zone,
                                                          volume_type=volume_type)

        volume_id = str(volume_response['volume']['id'])

        logger.info("create boot volume suc... volume id: %s, volume name: %s" % (volume_id, volume_name))

        if OpenstackClient.check_volume_status(auth_token, project_id, volume_id) == "available":
            return volume_response
        else:
            raise Exception(
                "create blank volume failed, volume status not available. volume_response: %s" % (str(volume_response)))

    @classmethod
    def attach_volume_to_instance(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        instance_id = kwargs['instance_id']
        volume_id = kwargs['volume_id']

        if OpenstackClient.check_instance_status(auth_token, project_id,
                                                 instance_id) == "ACTIVE" and OpenstackClient.check_volume_status(
                auth_token, project_id, volume_id) == "available":

            attach_response = OpenstackUtil.attachVolToInstance(auth_token, project_id, volume_id, instance_id)

            return attach_response

        else:
            raise Exception(
                'attach volume to instance failed, instance status not active or volume status not available')

    @classmethod
    def assgin_ip_to_instance(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        instance_name = kwargs['instance_name']
        instance_id = kwargs['instance_id']
        ext_network_id = kwargs['ext_network_id']
        network_name = kwargs['network_name']

        if OpenstackClient.check_instance_status(auth_token, project_id, instance_id) == "ACTIVE":

            instance_info = OpenstackUtil.getInstanceInfoById(auth_token, project_id, instance_id)

            fixed_ip = str(instance_info['server']['addresses'][network_name][0]['addr'])

            logger.info("get inner ip suc... inner network ip: %s" % (fixed_ip))
            logger.info("instance name: %s, inner ip: %s" % (instance_name, fixed_ip))

            floating_ip_info = OpenstackUtil.addNewRandomFloatingIp(auth_token=auth_token,
                                                                    network_id=ext_network_id,
                                                                    description=instance_name + "_ext_ip")
            floating_ip = str(floating_ip_info['floatingip']['id'])

            floating_ip_addr = str(floating_ip_info['floatingip']['floating_ip_address'])

            logger.info("random create a new floating ip suc... floating ip: %s" % (floating_ip))

            network_ports_info = OpenstackUtil.listNetworkPorts(auth_token=auth_token)
            for network_port in network_ports_info['ports']:

                port_id = str(network_port['id'])
                port_fixed_address = str(network_port['fixed_ips'][0]['ip_address'])

                if port_fixed_address == fixed_ip:
                    ip_response = OpenstackUtil.assginFloatingIpToInstance(auth_token=auth_token,
                                                                           floating_ip=floating_ip,
                                                                           port_id=port_id)

                    return ip_response
        else:
            raise Exception("assign ip to instance failed, instance status not active")

    @classmethod
    def check_instance_if_exist(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        name = kwargs['name']

        instances_info = OpenstackUtil.listInstances(auth_token, project_id)
        for instance in instances_info['servers']:
            instance_name = str(instance['name'])
            if instance_name.startswith(name):
                return True

        return False

    @classmethod
    def delete_instance_by_o_id(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        instance_id = kwargs['o_instance_id']

        OpenstackUtil.deleteInstanceById(auth_token=auth_token, project_id=project_id, instance_id=instance_id)

    @classmethod
    def delete_instance_by_name(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        name = kwargs['name']

        instances_info = OpenstackUtil.listInstances(auth_token, project_id)
        for instance in instances_info['servers']:
            instance_name = str(instance['name'])
            if (instance_name.startswith(name)) and (len(instance_name)-len(name) < 2):
                instance_id = str(instance['id'])
                OpenstackUtil.deleteInstanceById(auth_token=auth_token, project_id=project_id, instance_id=instance_id)
                time.sleep(1)
        OpenstackClient.delete_volume_by_name(kwargs=kwargs)

    @classmethod
    def delete_volume_by_name(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        name = kwargs['name']

        volumes_response = OpenstackUtil.listVolumes(auth_token, project_id)
        for volume in volumes_response['volumes']:
            volume_name = str(volume['name'])
            if volume_name.startswith(name):
                volume_id = str(volume['id'])
                OpenstackUtil.unattachVolFromInstanceByForce(auth_token, project_id, volume_id)
                time.sleep(1)
                OpenstackUtil.deleteVolumeById(auth_token, project_id, volume_id)

    @classmethod
    def delete_volume_by_o_id(cls, kwargs):

        auth_token = kwargs['auth_token']
        project_id = kwargs['project_id']
        volume_id = kwargs['o_volume_id']

        OpenstackUtil.unattachVolFromInstanceByForce(auth_token, project_id, volume_id)
        time.sleep(1)
        OpenstackUtil.deleteVolumeById(auth_token, project_id, volume_id)

    @classmethod
    def check_volume_status(cls, auth_token, project_id, volume_id):
        idx = 0
        while idx <= int(OpenstackConfig.OPENSTACK_CHECK_VOLUME_STATUS_RETRY_TIME):

            logger.info(
                "begin check volume status, project id: %s, volume id: %s" % (str(project_id), str(volume_id)))

            volume_info = OpenstackUtil.getVolumeInfoById(auth_token, project_id, volume_id)
            status = str(volume_info['volume']['status'])
            logger.info(
                "volume id: %s , name: %s, status: %s" % (
                    str(volume_id), str(volume_info['volume']['name']), str(status)))

            if status == "error":
                raise Exception("volume id: %s , name: %s, status: %s" % (
                    str(volume_id), str(volume_info['volume']['name']), str(status)))

            if idx == int(
                    OpenstackConfig.OPENSTACK_CHECK_VOLUME_STATUS_RETRY_TIME) or status == "available" or status == "error":
                return status

            logger.info("begin retry to check volume status...")
            time.sleep(OpenstackConfig.OPENSTACK_CHECK_VOLUME_STATUS_RETRY_INTERVAL)
            idx += idx

    @classmethod
    def check_instance_status(cls, auth_token, project_id, instance_id):
        idx = 0
        while idx <= int(OpenstackConfig.OPENSTACK_CHECK_INSTANCE_STATUS_RETRY_TIME):

            logger.info(
                "begin check instance status, project id: %s, instance id: %s" % (str(project_id), str(instance_id)))

            instance_info = OpenstackUtil.getInstanceInfoById(auth_token, project_id, instance_id)
            status = str(instance_info['server']['status'])
            logger.info(
                "instance id: %s , name: %s, status: %s" % (
                    str(instance_id), str(instance_info['server']['name']), str(status)))

            if status == "ERROR":
                raise Exception("instance id: %s , name: %s, status: %s" % (
                str(instance_id), str(instance_info['server']['name']), str(status)))

            if idx == int(
                    OpenstackConfig.OPENSTACK_CHECK_INSTANCE_STATUS_RETRY_TIME) or status == "ACTIVE" or status == "ERROR":
                return status

            logger.info("begin retry to check instance status...")
            time.sleep(OpenstackConfig.OPENSTACK_CHECK_VOLUME_STATUS_RETRY_INTERVAL)
            idx += idx

    @classmethod
    def create_instance(cls, kwargs):

        instance_info_list = []

        for i in range(1, int(int(kwargs['instance_num']) + 1)):

            volume_info_list = []

            kwargs['idx'] = str(i)
            kwargs['instance_name'] = str(kwargs['name']) + str(i)

            kwargs['boot_volume_name'] = str(str(kwargs['instance_name']) + "_boot_vol")

            boot_volume_response = OpenstackClient.create_boot_volume(kwargs=kwargs)
            kwargs['boot_volume_id'] = str(boot_volume_response['volume']['id'])

            volume_info_list.append(
                {"name": str(kwargs['boot_volume_name']), "o_volume_id": str(kwargs['boot_volume_id']),
                 "type": str(kwargs['boot_volume_type']), "bootable": True, "size": str(kwargs['boot_volume_size'])})

            instance_response = OpenstackClient.create_instance_by_boot_volume(kwargs=kwargs)
            kwargs['instance_id'] = str(instance_response['server']['id'])

            for j in range(1, int(int(kwargs['volume_num_every_instance']) + 1)):
                kwargs['blank_volume_name'] = str(str(kwargs['instance_name']) + "_vol" + str(j))

                blank_volume_response = OpenstackClient.create_blank_volume(kwargs=kwargs)

                kwargs['volume_id'] = str(blank_volume_response['volume']['id'])

                attach_response = OpenstackClient.attach_volume_to_instance(kwargs=kwargs)

                volume_info_list.append(
                    {"name": str(kwargs['blank_volume_name']), "o_volume_id": str(kwargs['volume_id']),
                     "type": str(kwargs['blank_volume_type']), "bootable": True,
                     "size": str(kwargs['volume_disk_size'])})

            ip_response = OpenstackClient.assgin_ip_to_instance(kwargs=kwargs)

            instance_info = {"instance_name": str(kwargs['instance_name']), "o_instance_id": str(kwargs['instance_id']),
                             "volumes": volume_info_list,
                             "inner_ip": str(ip_response['floatingip']['fixed_ip_address']),
                             "float_ip": str(ip_response['floatingip']['floating_ip_address'])}
            instance_info_list.append(instance_info)

        return instance_info_list


if __name__ == '__main__':

    try:
        auth_token = OpenstackClient.get_auto_token(username="toss", password="tostos1234")
    except Exception as e:
        raise Exception(e.message)

    project_name, project_id = OpenstackClient.get_project_name_and_id(auth_token=auth_token)

    auth_token, project_id = OpenstackClient.get_auto_token_and_project(project_name, username="tos", password="tostos123")

    OpenstackUtil.listNetwork(auth_token=auth_token)

    OpenstackClient.get_subnet_network(project_id=project_id, auth_token=auth_token)

    token_id2 = OpenstackClient.get_auto_token_and_project(project_name="TOS", username="tos", password="tostos123")
    pass
