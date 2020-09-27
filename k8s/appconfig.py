# -*- coding: utf-8 -*-

import sys
sys.path.append('./..')
from .k8sconfig import Settings

HARBOR_BASE_URL = Settings.HARBOR_BASE_URL
LICENSE_ADDRESS = Settings.LICENSE_ADDRESS
TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS = Settings.TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS
TRANSWARP_GUARDIAN_ADDRESS = Settings.TRANSWARP_GUARDIAN_ADDRESS


def get_cpu_limit(vcpus):
    val = float(vcpus) if float(vcpus) > float(3) else 1
    return val


def get_mem_limit(ram):
    val = 2 if float(ram) > float(12) else 1
    return val


def get_cpu_request():
    return 0.2


def get_mem_request():
    return 0.5


class K8sAppConfig(object):

    @classmethod
    def get_hdfs_app_config(cls, service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name):
        dict = {

            "hdfs_httpfs_image": str(HARBOR_BASE_URL + "httpfs" + ":" + service_tag) if images.get('httpfs_image', '') == '' else images.get('httpfs_image'),
            "hdfs_data_image": str(HARBOR_BASE_URL + "hdfs" + ":" + service_tag) if images.get('hdfs_image', '') == '' else images.get('hdfs_image'),
            "hdfs_journal_image": str(HARBOR_BASE_URL + "hdfs" + ":" + service_tag) if images.get('hdfs_image', '') == '' else images.get('hdfs_image'),
            "hdfs_name_image": str(HARBOR_BASE_URL + "hdfs" + ":" + service_tag) if images.get('hdfs_image', '') == '' else images.get('hdfs_image'),
            "hdfs_zkfc_image": str(HARBOR_BASE_URL + "hdfs" + ":" + service_tag) if images.get('hdfs_image', '') == '' else images.get('hdfs_image'),
            "zk_image": str(HARBOR_BASE_URL + "zookeeper" + ":" + service_tag) if images.get('zookeeper_image', '') == '' else images.get('zookeeper_image'),
            "LICENSE_ADDRESS": LICENSE_ADDRESS,
            "Customized_Namespace": tenant_name,

            "zk_cpu_limit": 1,
            "zk_memory_limit": 1,
            "hdfs_name_cpu_limit": 2 if float(vcpus) > float(3) else 1,
            "hdfs_name_memory_limit": get_mem_limit(ram),
            "hdfs_data_cpu_limit": get_cpu_limit(vcpus),
            "hdfs_data_memory_limit": float(ram) if float(ram) > float(4) else 2,
            "hdfs_journal_cpu_limit": get_cpu_limit(vcpus),
            "hdfs_journal_memory_limit":  float(ram) if float(ram) > float(4) else 1,
            "hdfs_zkfc_cpu_limit": 2 if float(vcpus) > float(3) else 1,
            "hdfs_httpfs_cpu_limit": 2 if float(vcpus) > float(3) else 1,
            "hdfs_httpfs_memory_limit": get_mem_limit(ram),
            "hdfs_zkfc_memory_limit": get_mem_limit(ram),

            "hdfs_zkfc_cpu_request": get_cpu_request(),
            "hdfs_zkfc_memory_request": get_mem_request(),
            "hdfs_httpfs_cpu_request": get_cpu_request(),
            "hdfs_httpfs_memory_request": get_mem_request(),
            "hdfs_name_cpu_request": get_cpu_request(),
            "hdfs_name_memory_request": get_mem_request(),
            "zk_cpu_request": 0.1,
            "zk_memory_request": get_mem_request(),
            "hdfs_data_cpu_request": get_cpu_request(),
            "hdfs_data_memory_request": get_mem_request(),
            "hdfs_journal_cpu_request": get_cpu_request(),
            "hdfs_journal_memory_request": get_mem_request()

        }

        if enable_kerberos:
            dict["Transwarp_Auto_Injected_Volumes"] = [{
                'kind': "Secret",
                'selector': {
                    "transwarp.keytab": secret_name,
                },
                'volumeName': "keytab",
            }]

            dict["Transwarp_Guardian_LDAP_Server_Address"] = TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS
            dict["Transwarp_Guardian_Address"] = TRANSWARP_GUARDIAN_ADDRESS
            dict["zk_mounted_kerberos"] = True
            dict["hdfs_mounted_kerberos"] = True

        return dict

    @classmethod
    def get_yarn_app_config(cls, service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name):

        dict = {
            "history_server_image": str(HARBOR_BASE_URL + "yarn" + ":" + service_tag) if images.get('yarn_image', '') == '' else images.get('yarn_image'),
            "node_manager_image": str(HARBOR_BASE_URL + "yarn" + ":" + service_tag) if images.get('yarn_image', '') == '' else images.get('yarn_image'),
            "timeline_server_image": str(HARBOR_BASE_URL + "yarn" + ":" + service_tag) if images.get('yarn_image', '') == '' else images.get('yarn_image'),
            "resource_manager_image": str(HARBOR_BASE_URL + "yarn" + ":" + service_tag) if images.get('yarn_image', '') == '' else images.get('yarn_image'),
            "LICENSE_ADDRESS": LICENSE_ADDRESS,
            "Customized_Namespace": tenant_name,

            "yarn_node_cpu_limit": get_cpu_limit(vcpus),
            "yarn_node_memory_limit": float(ram) if float(ram) > float(4) else 2,
            "yarn_rm_cpu_limit": 2 if float(vcpus) > float(3) else 1,
            "yarn_rm_memory_limit": 2 if float(ram) > float(4) else 2,

            "yarn_node_cpu_request": get_cpu_request(),
            "yarn_node_memory_request": get_mem_request(),
            "yarn_rm_cpu_request": get_cpu_request(),
            "yarn_rm_memory_request": get_mem_request()

        }

        if enable_kerberos:
            dict["Transwarp_Auto_Injected_Volumes"] = [{
                'kind': "Secret",
                'selector': {
                    "transwarp.keytab": secret_name,
                },
                'volumeName': "keytab",
            }]

            dict["Transwarp_Guardian_LDAP_Server_Address"] = TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS
            dict["Transwarp_Guardian_Address"] = TRANSWARP_GUARDIAN_ADDRESS

            dict["yarn_mounted_kerberos"] = True

        return dict

    @classmethod
    def get_inceptor_app_config(cls, service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name):

        dict = {
            "inceptor_executor_image": str(HARBOR_BASE_URL + "inceptor" + ":" + service_tag) if images.get('inceptor_image', '') == '' else images.get('inceptor_image'),
            "inceptor_master_image": str(HARBOR_BASE_URL + "inceptor" + ":" + service_tag) if images.get('inceptor_image', '') == '' else images.get('inceptor_image'),
            "metastore_image": str(HARBOR_BASE_URL + "inceptor" + ":" + service_tag) if images.get('inceptor_image', '') == '' else images.get('inceptor_image'),
            "mysql_image": str(HARBOR_BASE_URL + "inceptor" + ":" + service_tag) if images.get('inceptor_image', '') == '' else images.get('inceptor_image'),
            "LICENSE_ADDRESS": LICENSE_ADDRESS,
            "Customized_Namespace": tenant_name,

            "inceptor_master_cpu_limit": 2 if float(vcpus) > float(3) else 1,
            "inceptor_master_memory_limit": 2 if float(ram) > float(4) else 1,

            "inceptor_executor_cpu_limit": get_cpu_limit(vcpus),
            "inceptor_executor_memory_limit": float(ram) if float(ram) > float(4) else 2,

            "metastore_cpu_limit": 2 if float(vcpus) > float(3) else 1,
            "metastore_memory_limit":  2 if float(ram) > float(4) else 1,

            "mysql_cpu_limit": 1,
            "mysql_memory_limit": 1,

            "mysql_cpu_request": get_cpu_request(),
            "mysql_memory_request": get_mem_request(),
            "inceptor_master_cpu_request": get_cpu_request(),
            "inceptor_master_memory_request": get_mem_request(),
            "inceptor_executor_cpu_request": get_cpu_request(),
            "inceptor_executor_memory_request": get_mem_request(),
            "metastore_cpu_request": get_cpu_request(),
            "metastore_memory_request": get_mem_request()

        }

        if enable_kerberos:
            dict["Transwarp_Auto_Injected_Volumes"] = [{
                'kind': "Secret",
                'selector': {
                    "transwarp.keytab": secret_name,
                },
                'volumeName': "keytab",
            }]

            dict["Transwarp_Guardian_LDAP_Server_Address"] = TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS
            dict["Transwarp_Guardian_Address"] = TRANSWARP_GUARDIAN_ADDRESS
            dict["zk_mounted_kerberos"] = True
            dict["inceptor_mounted_kerberos"] = True

            dict["Metastore_Kerberos_Principal"] = "hive/tos@TDH"
            dict["Hive_Kerberos_Principal"] = "hive/tos@TDH"
            dict["Zookeeper_Kerberos_Principal"] = "zookeeper/tos"
            dict["inceptor_authentication"] = "KERBEROS"
            dict["hadoop_authentication"] = "kerberos"

        return dict

    @classmethod
    def get_hyperbase_app_config(cls, service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name):

         dict = {
                  "hbase_rest_image": str(HARBOR_BASE_URL + "hbase" + ":" + service_tag) if images.get('hbase_image', '') == '' else images.get('hbase_image'),
                  "hbase_thrift_image": str(HARBOR_BASE_URL + "hbase" + ":" + service_tag) if images.get('hbase_image', '') == '' else images.get('hbase_image'),
                  "hbase_master_image": str(HARBOR_BASE_URL + "hbase" + ":" + service_tag) if images.get('hbase_image', '') == '' else images.get('hbase_image'),
                  "hbase_rs_image": str(HARBOR_BASE_URL + "hbase" + ":" + service_tag) if images.get('hbase_image', '') == '' else images.get('hbase_image'),
                  "LICENSE_ADDRESS": LICENSE_ADDRESS,
                  "Customized_Namespace": tenant_name,

                  "hbase_master_cpu_request": get_cpu_request(),
                  "hbase_master_memory_request": get_mem_request(),
                  "hbase_rest_cpu_request": get_cpu_request(),
                  "hbase_rest_memory_request": get_mem_request(),
                  "hbase_rs_cpu_request": get_cpu_request(),
                  "hbase_rs_memory_request": get_mem_request(),
                  "hbase_thrift_cpu_request": get_cpu_request(),
                  "hbase_thrift_memory_request": get_mem_request(),

                  "hbase_master_cpu_limit": 2 if float(vcpus) > float(3) else 1,
                  "hbase_master_memory_limit": 2 if float(ram) > float(4) else 1,
                  "hbase_rest_cpu_limit": 1,
                  "hbase_rest_memory_limit": 1,
                  "hbase_rs_cpu_limit": get_cpu_limit(vcpus),
                  "hbase_rs_memory_limit": get_mem_limit(ram),
                  "hbase_thrift_cpu_limit": 1,
                  "hbase_thrift_memory_limit": 1
         }

         if enable_kerberos:
             dict["Transwarp_Auto_Injected_Volumes"] = [{
                 'kind': "Secret",
                 'selector': {
                     "transwarp.keytab": secret_name,
                 },
                 'volumeName': "keytab",
             }]

             dict["Transwarp_Guardian_LDAP_Server_Address"] = TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS
             dict["Transwarp_Guardian_Address"] = TRANSWARP_GUARDIAN_ADDRESS
             dict["hbase_mounted_kerberos"] = True

         return dict

    @classmethod
    def get_search_app_config(cls, service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name):

        dict = {

            "es_image": str(HARBOR_BASE_URL + "search" + ":" + service_tag) if images.get('search_image', '') == '' else images.get('search_image'),
            "es_head_image": str(HARBOR_BASE_URL + "search" + ":" + service_tag) if images.get('search_image', '') == '' else images.get('search_image'),
            "LICENSE_ADDRESS": LICENSE_ADDRESS,
            "Customized_Namespace": tenant_name,

            "es_client_cpu_limit": 1,
            "es_client_memory_limit": 1,
            "es_data_cpu_limit": get_cpu_limit(vcpus),
            "es_data_memory_limit": get_mem_limit(ram),
            "es_master_cpu_limit":  2 if float(vcpus) > float(3) else 1,
            "es_master_memory_limit": 2 if float(ram) > float(4) else 1,

            "es_client_cpu_request": get_cpu_request(),
            "es_client_memory_request": get_mem_request(),
            "es_data_cpu_request": get_cpu_request(),
            "es_data_memory_request": get_mem_request(),
            "es_master_cpu_request": get_cpu_request(),
            "es_master_memory_request": get_mem_request()

        }
        if enable_kerberos:

            dict["Transwarp_Auto_Injected_Volumes"] = [{
                'kind': "Secret",
                'selector': {
                    "transwarp.keytab": secret_name,
                },
                'volumeName': "keytab",
            }]

            dict["Transwarp_Guardian_LDAP_Server_Address"] = TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS
            dict["Transwarp_Guardian_Address"] = TRANSWARP_GUARDIAN_ADDRESS

        return dict

    @classmethod
    def get_sophon_app_config(cls, service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name):

        dict = {

            "sophon_server_image": str(HARBOR_BASE_URL + "sophon-server" + ":" + service_tag) if images.get('sophon_server_image', '') == '' else images.get('sophon_server_image'),
            "LICENSE_ADDRESS": LICENSE_ADDRESS,
            "Customized_Namespace": tenant_name,

            "sophon_cpu_request": get_cpu_request(),
            "sophon_memory_request":  get_mem_request(),
            "sophon_cpu_limit": get_cpu_limit(vcpus),
            "sophon_memory_limit": get_mem_limit(ram)
        }

        return dict

    @classmethod
    def get_txsql_app_config(cls, service_tag, tenant_name, ram, vcpus, images, enable_kerberos, secret_name):

        dict = {
            "txsql_image": str(HARBOR_BASE_URL + "mysql" + ":" + "tdc-1.0.0-rc5") if images.get('txsql_image', '') == '' else images.get('txsql_image'),
            "LICENSE_ADDRESS": LICENSE_ADDRESS,
            "Customized_Namespace": tenant_name,
            "txsql_cpu_limit": 1,
            "txsql_memory_limit": 1,
            "txsql_cpu_request":  get_cpu_request(),
            "txsql_memory_request": get_mem_request(),
            "txsql_replicas": 3,
            "txsql_rootpassword": "password"
        }

        if enable_kerberos:
            dict["Transwarp_Auto_Injected_Volumes"] = []
            dict["Transwarp_Guardian_LDAP_Server_Address"] = TRANSWARP_GUARDIAN_LDAP_SERVER_ADDRESS
            dict["Transwarp_Guardian_Address"] = TRANSWARP_GUARDIAN_ADDRESS

        return dict