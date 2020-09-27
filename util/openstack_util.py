# coding:utf-8
import json
import logging

from http_client import HttpClientUtil
from util.openstack_config import OpenstackConfig

logger = logging.getLogger(__name__)

class OpenstackUtil(object):
    @staticmethod
    def getAuthTokenAndProjectId(project_name, username, password):
        url = OpenstackConfig.OPENSTACK_IDENTITY_URL + "tokens"
        data = {
            "auth": {
                "tenantName": project_name,
                "passwordCredentials": {
                    "username": username,
                    "password": password
                }
            }
        }
        result = HttpClientUtil.doPost(url, json.dumps(data))
        content = json.loads(result.text)
        return str(content['access']['token']['id']), str(content['access']['token']['tenant']['id'])

    @staticmethod
    def listFlavors(auth_token, project_id):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/flavors"
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)

    @staticmethod
    def listImages(auth_token, project_id):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/images"
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)

    @staticmethod
    def listNetwork(auth_token):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "networks"
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)


    @staticmethod
    def listSubnetsNetwork(auth_token):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "subnets"
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)


    @staticmethod
    def listInstances(auth_token, project_id):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/servers"
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)

    @staticmethod
    def listFloatingIps(auth_token):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "floatingips"
        result = HttpClientUtil.doGet(url=url, auth_token=auth_token)

        return json.loads(result.text)

    @staticmethod
    def addNewRandomFloatingIp(auth_token, network_id, description="floating ip for tesing"):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "floatingips"
        data = {
            "floatingip": {
                "floating_network_id": str(network_id),
                "description": str(description)
            }
        }

        result = HttpClientUtil.doPost(url=url, auth_token=auth_token, data=json.dumps(data))
        return json.loads(result.text)

    @staticmethod
    def addNewSpecifiedFloatingIp(auth_token, network_id, floating_ip_address, description="floating ip for tesing"):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "floatingips"
        data = {
            "floatingip": {
                "floating_network_id": str(network_id),
                "floating_ip_address": str(floating_ip_address),
                "description": str(description)
            }
        }

        result = HttpClientUtil.doPost(url=url, auth_token=auth_token, data=json.dumps(data))
        return json.loads(result.text)

    @staticmethod
    def listNetworkPorts(auth_token):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "ports"
        result = HttpClientUtil.doGet(url=url, auth_token=auth_token)

        return json.loads(result.text)

    @staticmethod
    def getFloatingIpById(auth_token, floating_ip):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "floatingips/" + str(floating_ip)
        result = HttpClientUtil.doGet(url=url, auth_token=auth_token)

        return json.loads(result.text)

    @staticmethod
    def assginFloatingIpToInstance(auth_token, floating_ip, port_id):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "floatingips/" + str(floating_ip)
        data = {
            "floatingip": {
                "port_id": str(port_id)
            }
        }

        result = HttpClientUtil.doPut(url=url, auth_token=auth_token, data=json.dumps(data))
        return json.loads(result.text)

    @staticmethod
    def unassginFloatingIpFromInstance(auth_token, floating_ip):
        url = OpenstackConfig.OPENSTACK_NETWORK_URL + "floatingips/" + str(floating_ip)
        data = {
            "floatingip": {
                "port_id": None
            }
        }

        result = HttpClientUtil.doPut(url=url, auth_token=auth_token, data=json.dumps(data))
        return json.loads(result.text)

    @staticmethod
    def getInstanceInfoById(auth_token, project_id, instance_id):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/servers/" + str(instance_id)
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)

    @staticmethod
    def listProjects(auth_token):
        url = OpenstackConfig.OPENSTACK_IDENTITY_URL + "tenants"
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)

    @staticmethod
    def listVolumes(auth_token, project_id):
        url = OpenstackConfig.OPENSTACK_CINDER_URL + project_id + "/volumes"
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)

    @staticmethod
    def getVolumeInfoById(auth_token, project_id, volume_id):
        url = OpenstackConfig.OPENSTACK_CINDER_URL + project_id + "/volumes/" + str(volume_id)
        result = HttpClientUtil.doGet(url, auth_token)

        return json.loads(result.text)

    @staticmethod
    def createBlankVolume(auth_token, project_id, volume_name, volume_size, availability_zone="nova",
                          volume_type="lvmdriver-1"):
        url = OpenstackConfig.OPENSTACK_CINDER_URL + project_id + "/volumes"

        data = {
            "volume": {
                "size": int(volume_size),
                "description": str(volume_name + "_" + str(volume_size) + "G"),
                "name": str(volume_name),
                "metadata": {},
                "volume_type": str(volume_type),
                "availability_zone": str(availability_zone),
                "consistencygroup_id": None
            }
        }

        result = HttpClientUtil.doPost(url=url, data=json.dumps(data), auth_token=auth_token)
        return json.loads(result.text)

    @staticmethod
    def createBootVolumeByImage(auth_token, project_id, volume_name, volume_size, image_id, availability_zone="nova",
                                volume_type="lvmdriver-1"):
        url = OpenstackConfig.OPENSTACK_CINDER_URL + project_id + "/volumes"

        data = {
            "volume": {
                "size": int(volume_size),
                "description": str(volume_name + "_" + str(volume_size) + "G"),
                "name": str(volume_name),
                "metadata": {},
                "volume_type": str(volume_type),
                "availability_zone": str(availability_zone),
                "imageRef": str(image_id),
                "consistencygroup_id": None
            }

        }

        result = HttpClientUtil.doPost(url=url, data=json.dumps(data), auth_token=auth_token)
        return json.loads(result.text)

    @staticmethod
    def createMultiInstances(auth_token, project_id, instance_name, image_ref_id, flavor_ref_id, count, network_id,
                             security_group="default"):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/servers"

        data = {
            "server": {
                "name": str(instance_name),
                "imageRef": str(image_ref_id),
                "flavorRef": str(flavor_ref_id),
                "return_reservation_id": "True",
                "min_count": str(count),
                "max_count": str(count),
                "networks": [
                    {
                        "uuid": str(network_id)
                    }
                ],
                "security_groups": [
                    {
                        "name": str(security_group)
                    }
                ]
            }
        }

        result = HttpClientUtil.doPost(url=url, data=json.dumps(data), auth_token=auth_token)
        return json.loads(result.text)

    @staticmethod
    def createInstance(auth_token, project_id, instance_name, image_ref_id, flavor_ref_id, network_id, ipv4, user_data,
                       availability_zone="nova", security_group="default"):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/servers"

        data = {
            "server": {
                "name": str(instance_name),
                "imageRef": str(image_ref_id),
                "flavorRef": str(flavor_ref_id),
                "availability_zone": str(availability_zone),
                "OS-DCF:diskConfig": "AUTO",
                "networks": [
                    {
                        "uuid": str(network_id),
                        "fixed_ip": str(ipv4)
                    }
                ],
                "user_data": str(user_data),
                "security_groups": [
                    {
                        "name": str(security_group)
                    }
                ]
            }
        }

        result = HttpClientUtil.doPost(url=url, data=json.dumps(data), auth_token=auth_token)
        return json.loads(result.text)

    @staticmethod
    def createInstanceFromVolumeWithFixedIp(auth_token, project_id, instance_name, image_ref_id, flavor_ref_id, network_id, ipv4,
                                 volume_id, volume_size, user_data, availability_zone="nova", security_group="default"):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/servers"

        data = {
            "server": {
                "name": str(instance_name),
                "imageRef": str(image_ref_id),
                "flavorRef": str(flavor_ref_id),
                "availability_zone": str(availability_zone),
                "OS-DCF:diskConfig": "AUTO",
                "networks": [
                    {
                        "uuid": str(network_id),
                        "fixed_ip": str(ipv4)
                    }
                ],
                "security_groups": [
                    {
                        "name": str(security_group)
                    }
                ],
                "user_data": str(user_data),
                "block_device_mapping_v2": [{
                    "boot_index": "0",
                    "uuid": str(volume_id),
                    "source_type": "volume",
                    "volume_size": str(volume_size),
                    "destination_type": "volume",
                    "delete_on_termination": True
                }]
            }
        }

        result = HttpClientUtil.doPost(url=url, data=json.dumps(data), auth_token=auth_token)
        return json.loads(result.text)

    @staticmethod
    def createInstanceFromVolume(auth_token, project_id, instance_name, image_ref_id, flavor_ref_id, network_id, volume_id, volume_size, user_data, availability_zone="nova", security_group="default"):

        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/servers"

        data = {
            "server": {
                "name": str(instance_name),
                "imageRef": str(image_ref_id),
                "flavorRef": str(flavor_ref_id),
                "availability_zone": str(availability_zone),
                "OS-DCF:diskConfig": "AUTO",
                "networks": [
                    {
                        "uuid": str(network_id)
                    }
                ],
                "security_groups": [
                    {
                        "name": str(security_group)
                    }
                ],
                "user_data": str(user_data),
                "block_device_mapping_v2": [{
                    "boot_index": "0",
                    "uuid": str(volume_id),
                    "source_type": "volume",
                    "volume_size": str(volume_size),
                    "destination_type": "volume",
                    "delete_on_termination": False
                }]
            }
        }

        result = HttpClientUtil.doPost(url=url, data=json.dumps(data), auth_token=auth_token)
        return json.loads(result.text)

    @staticmethod
    def attachVolToInstance(auth_token, project_id, volume_id, instance_id):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + "/servers/" + str(instance_id) + "/os-volume_attachments"

        data = {
            "volumeAttachment": {
                "volumeId": str(volume_id)
            }
        }

        result = HttpClientUtil.doPost(url, data=json.dumps(data), auth_token=auth_token)

        return result

    @staticmethod
    def unattachVolFromInstanceByForce(auth_token, project_id, volume_id):
        url = OpenstackConfig.OPENSTACK_CINDER_URL + project_id + "/volumes/" + str(volume_id) + "/action"

        data = {
            "os-force_detach": {}
        }

        result = HttpClientUtil.doPost(url, data=json.dumps(data), auth_token=auth_token)

        return result

    @staticmethod
    def unattachVolFromInstance(auth_token, project_id, instance_id, volume_id):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + "/servers/" + str(instance_id) + "/os-volume_attachments/" + str(
            volume_id)

        result = HttpClientUtil.doDelete(url, auth_token=auth_token)

        return result

    @staticmethod
    def deleteVolumeById(auth_token, project_id, volume_id):
        url = OpenstackConfig.OPENSTACK_CINDER_URL + project_id + "/volumes/" + str(volume_id)
        result = HttpClientUtil.doDelete(url, auth_token=auth_token)

        return result

    @staticmethod
    def forceDeleteVolumeById(auth_token, project_id, volume_id):
        url = OpenstackConfig.OPENSTACK_CINDER_URL + project_id + "/volumes/" + str(volume_id) + "/action"

        data = {
            "os-force_delete": {}
        }

        result = HttpClientUtil.doPost(url, data=json.dumps(data), auth_token=auth_token)

        return result

    @staticmethod
    def deleteInstanceById(auth_token, project_id, instance_id):
        url = OpenstackConfig.OPENSTACK_NOVA_URL + project_id + "/servers/" + str(instance_id)
        result = HttpClientUtil.doDelete(url, auth_token=auth_token)

        return result

    @classmethod
    def getAuthTokenId(cls, username, password):

        url = OpenstackConfig.OPENSTACK_IDENTITY_URL + "tokens"
        data = {
            "auth": {
                "passwordCredentials": {
                    "username": username,
                    "password": password
                }
            }
        }
        result = HttpClientUtil.doPost(url, json.dumps(data))
        content = json.loads(result.text)
        return str(content['access']['token']['id'])

    @classmethod
    def verifyLoginUser(cls, username, password):

        try:
            auth_token = OpenstackUtil.getAuthTokenId(username=username, password=password)
        except Exception as e:
            return str(e.message), 401

        return "Login Success", 200


if __name__ == '__main__':


    auth_token = OpenstackUtil.getAuthTokenId("tos", "tostos123")
    OpenstackUtil.listProjects(auth_token)
    aa = OpenstackUtil.listNetwork(auth_token=auth_token)

    auth_token, project_id = OpenstackUtil.getAuthTokenAndProjectId("TOS", "tos", "tostos123")
    OpenstackUtil.listFloatingIps(auth_token=auth_token)
    OpenstackUtil.listNetwork(auth_token=auth_token)
    OpenstackUtil.addNewRandomFloatingIp(auth_token=auth_token, network_id="b67a6fab-b2ea-4f78-a2ca-1af21a7fad77",
                                         description="test")
    OpenstackUtil.addNewSpecifiedFloatingIp(auth_token=auth_token, network_id="b67a6fab-b2ea-4f78-a2ca-1af21a7fad77",
                                            floating_ip_address="172.24.4.250", description="test")
    OpenstackUtil.unassginFloatingIpFromInstance(auth_token=auth_token,
                                                 floating_ip="d05a1d24-8882-4a4f-8402-86ee9f241641")
    OpenstackUtil.assginFloatingIpToInstance(auth_token=auth_token, floating_ip="d05a1d24-8882-4a4f-8402-86ee9f241641",
                                             port_id="02540a6d-b90b-4604-ae89-a0bf90235510")
    # OpenstackUtil.listFlavors(auth_token, project_id)
    # OpenstackUtil.listImages(auth_token, project_id)
    # OpenstackUtil.listNetwork(auth_token)
    # OpenstackUtil.listInstances(auth_token, project_id)

    # OpenstackUtil.listVolumes(auth_token, project_id)

    # OpenstackUtil.addNewVolume(auth_token, project_id, "xxxx", 1, volume_type="lvmdriver-1")

    # OpenstackUtil.attachVolToInstance(auth_token, project_id, "1aa27443-a351-4377-985e-e1d0542ab835", "d62b6308-1c2c-4c68-b831-5cf2cbca866d",mount_point="dev/vdf")
    # OpenstackUtil.unattachVolFromInstance(auth_token, project_id, "1aa27443-a351-4377-985e-e1d0542ab835")
    # OpenstackUtil.deleteVolumeById(auth_token, project_id, "52917fd8-227f-441a-9076-c4a3a8d0920e")
    # OpenstackUtil.deleteInstanceById(auth_token, project_id, "d62b6308-1c2c-4c68-b831-5cf2cbca866d")
    # OpenstackUtil.createNewInstances(auth_token, project_id, instance_name="test", image_ref_id="7bf70c33-a8b1-4d51-8434-356e690c3f2f", flavor_ref_id="84", count=3, network_id="3141e152-eb3c-4024-a17a-221e12584d53")
