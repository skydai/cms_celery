# coding:utf-8

import logging
import uuid

from libappadapter import AppConfig, get_constraint_app_templates, get_kube_configs_from_template
from tdc_commons.k8s import k8s_base_config

from appconfig import K8sAppConfig
#from appsecret import K8sAppSecret
from k8s_depencies import K8sDependencies
from k8sconfig import Settings

logger = logging.getLogger(__name__)


class K8sService(object):

    @classmethod
    def create_service(cls, params):

        service_name = str(params.get('service_name'))
        service_tag = str(params.get('service_tag'))
        ram = str(params.get('ram', '1'))
        vcpus = str(params.get('vcpus', '1'))
        tenant_name = str(params.get('tenant_name', 'argon' + str(str(uuid.uuid4())[0:4])))
        images = params.get("images", {})
        enable_kerberos = bool(params.get("enable_kerberos", False))

        service_list = K8sDependencies.get_dependencies(service_tag, str(service_name).upper())
        if service_list == []:
            raise Exception("cannot found service depencies by: " + str(service_name).upper())

        k8s_base_config.kubernetes_host = Settings.KUBERNETES_ADDRESS
        k8s_base_config.debug = True

        from tdc_commons.k8s.operator import KubeTenantOp, KubeInstanceOp, KubeSecretOp
        tenantOp = KubeTenantOp()
        instanceOp = KubeInstanceOp()
        secretOp = KubeSecretOp()

        if not tenantOp.get_tenant(tenant_name) is None:
            raise Exception("tenant_name alreay exists !!!")

        tenantOp.create_tenant(tenant_name)

        apps_list = []
        for service in service_list:

            secret_name = str(tenant_name + "-" + str(service).lower() + "-secret")

            if enable_kerberos:
                logger.info("begin create secret for " + str(service))
                secret = K8sService.create_secret(str(service).upper(), tenant_name, secret_name)
                if secret != "":
                    secretOp.create_secret(tenant_name=tenant_name, secret_data=secret)
                logger.info("create secret success for " + str(service))

            tmp_ram = 2
            tmp_vcpus = 1

            if str(service).upper() == str(service_name).upper():
                tmp_ram = ram
                tmp_vcpus = vcpus

            tmp_app = AppConfig(str(service).lower(), str(service).upper(), version=K8sService.get_app_version(str(service).upper()),
                                 app_config=K8sService.get_app_config(str(service).upper(), service_tag, images, tenant_name, tmp_ram, tmp_vcpus, enable_kerberos, secret_name))
            apps_list.append(tmp_app)

        templates = get_constraint_app_templates(
            apps=apps_list,
            auto_relation=True
        )

        kube_app_configs = []
        for key, template in templates.items():
            kube_app_configs.append(get_kube_configs_from_template(template=template))

        logger.info("=================================")
        logger.info("namespace: " + tenant_name)
        logger.info("=================================")

        exist_instances_list = instanceOp.get_instances(tenant_name)
        if exist_instances_list != []:
            raise Exception("instance alreay exists !!! namespaces: %s" %(tenant_name))
            # for exist_instance in exist_instances_list:
            #     instanceOp.delete_instances(tenant_name, instance_name=str(exist_instance.instance_name))

        for app_config in kube_app_configs:
            instanceOp.create_instances(tenant_name, app_config)

        return tenant_name

    @classmethod
    def get_app_version(cls, service_name):

        if str(service_name) == "SOPHON":
            return '3.3'
        else:
            return '5.1'

    @classmethod
    def get_app_config(cls, service_name, service_tag, images, tenant_name, ram, vcpus, enable_kerberos, secret_name):

        if service_name == "INCEPTOR":
            return K8sAppConfig.get_inceptor_app_config(service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name)

        if service_name == "HYPERBASE":
            return K8sAppConfig.get_hyperbase_app_config(service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name)

        if service_name == "SEARCH":
            return K8sAppConfig.get_search_app_config(service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name)

        if service_name == "SOPHON":
           return K8sAppConfig.get_sophon_app_config(service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name)

        if service_name == "TXSQL":
            return K8sAppConfig.get_txsql_app_config(service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name)

        if service_name == "HDFS":
            return K8sAppConfig.get_hdfs_app_config(service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name)

        if service_name == "YARN":
            return K8sAppConfig.get_yarn_app_config(service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name)

    @classmethod
    def create_secret(cls, service_name, tenant_name, secret_name):

        if service_name == "INCEPTOR":
            principal_list = ["hive/tos", "HTTP/tos"]

        if service_name == "HYPERBASE":
            principal_list = ["hbase/tos", "HTTP/tos"]

        if service_name == "SEARCH":
            principal_list = ["es/tos"]

        if service_name == "TXSQL":
            return ""

        if service_name == "HDFS":
            principal_list = ["zookeeper/tos", "hdfs/tos", "HTTP/tos"]

        if service_name == "YARN":
            principal_list = ["yarn/tos", "mapred/tos", "HTTP/tos"]

        #return K8sAppSecret.create_service_secret(service_name, tenant_name, principal_list, secret_name)
        return ""


if __name__ == '__main__':
    params = {'service_name': 'INCEPTOR', 'ram': '1', 'service_tag': 'transwarp-5.2', 'vcpus': '1', 'tenant_name': 'argon0a7d',
     'enable_kerberos': True}

    K8sService.create_service(params=params)