# coding:utf-8
import json
import logging
import os
import traceback
import uuid
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from cmsconfig import UPDATE_OPENSTACK_SERVICE, UPDATE_OPENSTACK_NODE
from util.http_client import HttpClientUtil
from util.openstack_client import OpenstackClient

from util.tdhcluster_util import TdhClusterUtil

logger = logging.getLogger(__name__)


class OpenstackService(object):

    @classmethod
    def verify_openstack_user(cls, params):
        username = str(params.get('o_username', ''))
        password = str(params.get('o_password', ''))

        return OpenstackClient.verify_login_user(username=username, password=password)

    @classmethod
    def delete_instance(cls, params):

        kwargs = dict()
        kwargs['name'] = str(params.get('instance_name', ''))

        if kwargs['name'] == "":
            raise Exception("instance_name cannot be null")

        kwargs['username'] = str(params.get('o_username'))
        kwargs['password'] = str(params.get('o_password'))

        # 1. login in
        auth_token = OpenstackClient.get_auto_token(kwargs['username'], kwargs['password'])
        project_name, project_id = OpenstackClient.get_project_name_and_id(auth_token=auth_token)

        auth_token, project_id = OpenstackClient.get_auto_token_and_project(project_name, kwargs['username'],
                                                                            kwargs['password'])

        kwargs['auth_token'] = auth_token
        kwargs['project_id'] = project_id
        kwargs['project_name'] = project_name

        OpenstackClient.delete_instance_by_name(kwargs=kwargs)



    @classmethod
    def create_instance(cls, params):

        # return {'service_list': 'INCEPTOR', 'nodes': [
        #     {'name': 'lisong3f6d1', 'hostname': 't322d01', 'inner_ip': '10.0.10.45', 'username': 'root',
        #      'float_ip': '172.16.132.31', 'password': 'transwarp123'},
        #     {'name': 'lisong3f6d2', 'hostname': 't322d02', 'inner_ip': '10.0.10.19', 'username': 'root',
        #      'float_ip': '172.16.132.44', 'password': 'transwarp123'},
        #     {'name': 'lisong3f6d3', 'hostname': 't322d03', 'inner_ip': '10.0.10.17', 'username': 'root',
        #      'float_ip': '172.16.132.32', 'password': 'transwarp123'}], 'email': 'lisong.qiu@transwarp.io',
        #  'tdh_version': 'transwarp-5.1.2-rc3'}

        kwargs = dict()
        kwargs['name'] = str(params.get('name', ''))

        kwargs['boot_volume_type'] = str(params.get('boot_volume_type', 'ssd'))
        kwargs['volume_num_every_instance'] = int(params.get('volume_num_every_instance', 1))

        kwargs['o_image_id'] = str(params.get('o_image_id', ''))
        kwargs['o_flavor_id'] = str(params.get('o_flavor_id', ''))

        kwargs['volume_disk_size'] = str(params.get('volume_disk_size', '100'))

        kwargs['blank_volume_type'] = str(params.get('blank_volume_type', 'lvm'))
        kwargs['instance_num'] = str(params.get('instance_num', 1))

        kwargs['volume_availabiliity_zone'] = 'nova'
        kwargs['boot_volume_availabiliity_zone'] = 'nova'

        kwargs['username'] = str(params.get('o_username'))
        kwargs['password'] = str(params.get('o_password'))

        kwargs['creator'] = str(kwargs['username'])
        kwargs['modifier'] = str(kwargs['username'])

        kwargs['boot_volume_size'] = str(params.get('boot_volume_size'))

        instance_num = int(kwargs['instance_num'])

        date = str(params.get('date', 'latest'))
        email = str(params.get('email', 'youzhi.su@transwarp.io'))
        pre_hostname = str(params.get('pre_hostname', ''))
        if not pre_hostname.strip():
            pre_hostname = 't' + str(uuid.uuid1())[0:4]

        # 1. login in
        auth_token = OpenstackClient.get_auto_token(kwargs['username'], kwargs['password'])
        project_name, project_id = OpenstackClient.get_project_name_and_id(auth_token=auth_token)

        auth_token, project_id = OpenstackClient.get_auto_token_and_project(project_name, kwargs['username'],
                                                                            kwargs['password'])

        kwargs['auth_token'] = auth_token
        kwargs['project_id'] = project_id
        kwargs['project_name'] = project_name

        sub_network_id, sub_network_name = OpenstackClient.get_subnet_network(project_id=project_id,
                                                                              auth_token=auth_token)
        kwargs['inner_network_id'] = str(sub_network_id)
        kwargs['network_name'] = str(sub_network_name)

        kwargs['ext_network_id'] = str("47018791-c1a3-4284-a584-9d37b2bcbadc")

        # 2. check instance if exits
        if OpenstackClient.check_instance_if_exist(kwargs=kwargs):
            logger.error("instance name already exists...")
            raise Exception(str(kwargs['name']) + " instance name already exists...")

        # 3. create instances
        instance_info_list = OpenstackClient.create_instance(kwargs=kwargs)

        inner_ip_list = []
        node_list = []
        for instance_info in instance_info_list:
            inner_ip_list.append(str(instance_info['inner_ip']))
            node_list.append({"username": "root", "password": "transwarp123", "name": str(instance_info['instance_name']), "float_ip":str(instance_info['float_ip']), "inner_ip":str(instance_info['inner_ip'])})

        username = "root"
        password = "transwarp123"
        nodes = []
        for i in range(instance_num):
            name = node_list[i]["name"]
            hostname = ""
            float_ip = node_list[i]["float_ip"]
            inner_ip = node_list[i]["inner_ip"]
            node = {"name": name, "hostname": hostname, "float_ip": float_ip, "inner_ip": inner_ip, "username": username,
                    "password": password}
            nodes.append(node)

        tmp_dict = {
            "nodes": nodes,
            "pre_hostname": pre_hostname,
            "tdh_version": str(params.get('tdh_version', '')),
            "service_list": str(
                params.get('service_list', 'INCEPTOR')),
            "date": date,
            "email": email
        }

        return tmp_dict

    @classmethod
    def install_manager(cls, params):

        """
            install tdh manager
        """
        # return {'service_list': 'INCEPTOR', 'nodes': [
        #     {'name': 'lisong3f6d1', 'hostname': 't322d01', 'inner_ip': '10.0.10.45', 'username': 'root',
        #      'float_ip': '172.16.132.31', 'password': 'transwarp123'},
        #     {'name': 'lisong3f6d2', 'hostname': 't322d02', 'inner_ip': '10.0.10.19', 'username': 'root',
        #      'float_ip': '172.16.132.44', 'password': 'transwarp123'},
        #     {'name': 'lisong3f6d3', 'hostname': 't322d03', 'inner_ip': '10.0.10.17', 'username': 'root',
        #      'float_ip': '172.16.132.32', 'password': 'transwarp123'}], 'email': 'lisong.qiu@transwarp.io',
        #  'tdh_version': 'transwarp-5.1.2-rc3'}

        nodes = params.get('nodes')
        remote_ip = str(params.get('ext_manager_ip', nodes[0]["float_ip"]))
        remote_manager_ip = str(params.get('inner_manager_ip', nodes[0]["inner_ip"]))
        remote_user = str(params.get('username', nodes[0]["username"]))
        remote_password = str(params.get('password', nodes[0]["password"]))

        service_list = str(params.get('service_list', 'TOS,LICENSE_SERVICE,ZOOKEEPER,HDFS,YARN,TXSQL,GUARDIAN,INCEPTOR'))
        tdh_version = str(params.get('tdh_version'))
        manager_version = str(params.get('manager_version'))

        inner_ips = ','.join(str(node['inner_ip']) for node in nodes)

        date = str(params.get('date', 'latest'))
        email = str(params.get('email', 'youzhi.su@transwarp.io'))
        pre_hostname = str(params.get('pre_hostname', ''))

        if not pre_hostname.strip():
            pre_hostname = 't' + str(uuid.uuid1())[0:4]

        index = 0
        for node in nodes:
            hostname = pre_hostname + '0' + str(index + 1)
            index = index + 1
            node["hostname"] = hostname

        script_path = str(TdhClusterUtil.get_project_path() + "/scripts/")
        os.system('ssh-keygen -f "~/.ssh/known_hosts" -R ' + str(remote_ip))
        remote_file = "/tmp/pre_install.sh"
        local_file = str(script_path + "pre_install.sh")
        try:
            scp_flag = TdhClusterUtil.scp_file_to_remote(hostname=remote_ip, username=remote_user, password=remote_password,
                                                         local_file=local_file, remote_file=remote_file, port=22)
            if not scp_flag:
                logger.error(
                    "scp %s to %s@%s:%s, password: %s" % (local_file, remote_user, remote_ip, remote_file, remote_password))
                raise Exception("scp file to manager failed, scp %s to %s@%s:%s, password: %s" % (
                local_file, remote_user, remote_ip, remote_file, remote_password))

            pre_install_script = str("cd /tmp; sh -x pre_install.sh %s 2>&1 > /tmp/pre_install.log" % (tdh_version))
            pre_install_exit_code = TdhClusterUtil.exec_remote_script(hostname=remote_ip, username=remote_user,
                                                                      password=remote_password,
                                                                      shell_script=pre_install_script)
            if pre_install_exit_code != 0:
                logger.error("exec remote pre_install script fail, remote_ip: %s, remote_user: %s, remote_password: %s" % (
                remote_ip, remote_user, remote_password))
                logger.error("unzip script: %s" % (pre_install_script))
                raise Exception("unzip pre_install script failed. pre_install_script: %s" % str(pre_install_script))

            remote_log_file = "/tmp/auto_web_install/auto_web_install.log"

            install_manager_script = str(
                "cd /tmp/auto_web_install; sh -x install.sh --manager_ip %s --node_ips \"%s\" --node_password %s --tdh_version %s --manager_version %s --date %s --pre_hostname %s" % (
                    remote_manager_ip, inner_ips, remote_password, tdh_version, manager_version, date, pre_hostname))
            logger.info("install manager script: %s" % (install_manager_script))

            logger.info("*************************************************")
            logger.info("install manager script: " + str(install_manager_script))
            logger.info("*************************************************")

            install_manager_script = str(install_manager_script + " 2>&1 >" + remote_log_file)

            install_manager_exit_code = TdhClusterUtil.exec_remote_script(hostname=remote_ip, username=remote_user,
                                                                          password=remote_password,
                                                                          shell_script=install_manager_script)

            # local_log_file = str(TdhClusterUtil.get_project_path() + "/auto_web_install.log")
            # if not TdhClusterUtil.scp_remote_file_to_local(hostname=remote_ip, username=remote_user,
            #                                                password=remote_password, remote_file=remote_log_file,
            #                                                local_file=local_log_file, port=22):
            #     logger.error("scp remote auto ui intall log to local fail...")
            #     raise

            if install_manager_exit_code != 0:
                logger.error(
                    "exec remote install manager script fail, remote_ip: %s, remote_user: %s, remote_password: %s" % (
                        remote_ip, remote_user, remote_password))
                logger.error("install manager script: %s" % (install_manager_script))
                raise Exception(
                    "exec remote install manager script fail,remote_ip: %s, remote_user: %s, remote_password: %s" % (
                        remote_ip, remote_user, remote_password))



            tmp_dict = {
                "tdh_version": tdh_version,
                "manager_version": manager_version,
                "nodes": nodes,
                "service_list": service_list,
                "email": email
            }

            return tmp_dict

        except Exception, e:
            logger.error('traceback.format_exc(): %s' % str(traceback.format_exc()))
            logger.error(e)
            raise Exception('traceback.format_exc(): %s' % str(traceback.format_exc()))

    @classmethod
    def install_service(cls, params):
        """
            install tdh service
        """
        # raise

        nodes = params.get('nodes')
        remote_ip = str(params.get('ext_manager_ip', nodes[0]["float_ip"]))
        remote_manager_ip = str(params.get('inner_manager_ip', nodes[0]["inner_ip"]))
        remote_user = str(params.get('username', nodes[0]["username"]))
        remote_password = str(params.get('password', nodes[0]["password"]))
        inner_ips = ','.join(str(node['inner_ip']) for node in nodes)

        tdh_version = tdh_metainfo = str(params.get('tdh_version'))


        service_list = str(params.get('service_list', 'TOS,LICENSE_SERVICE,ZOOKEEPER,HDFS,YARN,TXSQL,INCEPTOR'))
        service_list = cls.getdependencies(tdh_version, service_list)
        email = str(params.get('email', 'youzhi.su@transwarp.io'))
        RegistryLocation = ""
        if tdh_version.startswith("transwarp-6"):
            RegistryLocation="/tmp/transwarp/TDH-Image-Registry-Transwarp-" + tdh_version.split('-', 1)[1] + ".tar.gz"

        try:

            unzip_script = str(
                "[ -e /opt/TDHAutoInstall ] && rm -rf /opt/TDHAutoInstall; cd /opt; tar -zxvf TDHAutoInstall.tar.gz")
            unzip_exit_code = TdhClusterUtil.exec_remote_script(hostname=remote_ip, username=remote_user,
                                                                password=remote_password,
                                                                shell_script=unzip_script)
            if unzip_exit_code != 0:
                logger.error(
                    "exec remote unzip script fail, remote_ip: %s, remote_user: %s, remote_password: %s" % (
                        remote_ip, remote_user, remote_password))
                logger.error("unzip script: %s" % (unzip_script))
                raise Exception("exec remote unzip script fail, remote_ip: %s, remote_user: %s, remote_password: %s" % (
                    remote_ip, remote_user, remote_password))

            remote_log_file = "/opt/TDHAutoInstall/auto_service_install.log"

            if str(tdh_version).startswith("transwarp-4"):

                install_service_script = str(
                    "cd /opt/TDHAutoInstall; sh -x tdh_auto_install.sh --manager_ip  %s --node_ips \"%s\"  --node_password %s  --tdh_service \"%s\" -y >%s 2>&1 " % (
                        remote_manager_ip, inner_ips, remote_password, service_list, remote_log_file))
            elif str(tdh_version).startswith("transwarp-6"):
                install_service_script = str(
                    "cd /opt/TDHAutoInstall; sh -x tdh_auto_install.sh --manager_ip  %s --node_ips \"%s\"  --node_password %s --RegistryLocation %s --guest_phone 000000000 --tdh_metainfo %s --tdh_service \"%s\" -y >%s 2>&1 " % (
                        remote_manager_ip, inner_ips, remote_password, RegistryLocation, tdh_metainfo, service_list, remote_log_file))
            else:
                install_service_script = str(
                    "cd /opt/TDHAutoInstall; sh -x tdh_auto_install.sh --manager_ip  %s --node_ips \"%s\"  --node_password %s --guest_phone 000000000 --tdh_metainfo %s --tdh_service \"%s\" -y >%s 2>&1 " % (
                        remote_manager_ip, inner_ips, remote_password, tdh_metainfo, service_list, remote_log_file))

            logger.info("***************************************************************")
            logger.info("install TDH service script: " + str(install_service_script))
            logger.info("***************************************************************")

            install_service_exit_code = TdhClusterUtil.exec_remote_script(hostname=remote_ip,
                                                                          username=remote_user,
                                                                          password=remote_password,
                                                                          shell_script=install_service_script)

            if install_service_exit_code != 0:
                logger.error(
                    "exec remote install service script fail, remote_ip: %s, remote_user: %s, remote_password: %s" % (
                        remote_ip, remote_user, remote_password))
                logger.error("install service script: %s" % (install_service_exit_code))
                raise Exception("exec remote install service script fail, remote_ip: %s, remote_user: %s, remote_password: %s" % (
                        remote_ip, remote_user, remote_password))

            data_dict = {
                    "username": remote_user,
                    "manager_ip": remote_ip,
                    "tdh_version": tdh_version,
                    "nodes": nodes,
                    "service_list": service_list,
                    "email": email
            }

            return data_dict

        except Exception, e:
            logger.error('traceback.format_exc(): %s' % str(traceback.format_exc()))
            logger.error(e)
            raise Exception('traceback.format_exc(): %s' % str(traceback.format_exc()))

    @classmethod
    def getdependencies(cls, tdh_version, install_list):

        # contruct prerequisites
        # [0, 1] to install 0, you must install 1 first
        # eg: service_install_list zookeeper, hdfs, yarn
        # GUARDIAN
        service_install_list = install_list.split(',')
        prerequisites = []
        service_lists = []
        AllService = {}
        if 'transwarp-4.9' in tdh_version:
            AllService = {'ZOOKEEPER', 'HDFS', 'KAFKA', 'OOZIE', 'HYPERBASE', 'YARN', 'ES', 'OOZIE', 'INCEPTOR', 'STREAM',
                      'SQOOP', 'DISCOVER', 'HUE', 'GUARDIAN', 'TRANSPEDIA'}
            AllServiceLength = len(AllService)
            prerequisites.append(['HDFS', 'ZOOKEEPER'])
            prerequisites.append(['KAFKA', 'ZOOKEEPER'])
            prerequisites.append(['YARN', 'HDFS'])
            prerequisites.append(['OOZIE', 'HDFS'])
            prerequisites.append(['HYPERBASE', 'HDFS'])
            prerequisites.append(['HYPERBASE', 'ES'])
            prerequisites.append(['GUARDIAN', 'YARN'])
            prerequisites.append(['INCEPTOR', 'ES'])
            prerequisites.append(['INCEPTOR', 'GUARDIAN'])
            prerequisites.append(['STREAM', 'YARN'])
            prerequisites.append(['SQOOP', 'YARN'])
            prerequisites.append(['DISCOVER', 'YARN'])
            prerequisites.append(['HUE', 'YARN'])
            prerequisites.append(['HUE', 'OOZIE'])
            prerequisites.append(['TRANSPEDIA', 'ES'])

        elif 'sophon' in tdh_version:
            AllService = {'TOS', 'LICENSE_SERVICE', 'ZOOKEEPER', 'HDFS', 'YARN', 'HYPERBASE', 'TXSQL', 'SEARCH',
                          'GUARDIAN', 'INCEPTOR'}
            AllServiceLength = len(AllService)
            prerequisites.append(['LICENSE_SERVICE', 'TOS'])
            prerequisites.append(['ZOOKEEPER', 'LICENSE_SERVICE'])
            prerequisites.append(['HDFS', 'ZOOKEEPER'])
            prerequisites.append(['YARN', 'HDFS'])
            prerequisites.append(['SEARCH', 'YARN'])
            prerequisites.append(['HYPERBASE', 'SEARCH'])
            prerequisites.append(['TXSQL', 'HDFS'])
            prerequisites.append(['GUARDIAN', 'TXSQL'])
            prerequisites.append(['INCEPTOR', 'GUARDIAN'])

        elif 'transwarp-ce' in tdh_version:
            AllService = {'TOS', 'LICENSE_SERVICE', 'ZOOKEEPER', 'HDFS', 'YARN', 'HYPERBASE', 'TXSQL', 'INCEPTOR'}
            AllServiceLength = len(AllService)
            prerequisites.append(['LICENSE_SERVICE', 'TOS'])
            prerequisites.append(['ZOOKEEPER', 'LICENSE_SERVICE'])
            prerequisites.append(['HDFS', 'ZOOKEEPER'])
            prerequisites.append(['YARN', 'HDFS'])
            prerequisites.append(['HYPERBASE', 'YARN'])
            prerequisites.append(['TXSQL', 'YARN'])
            prerequisites.append(['INCEPTOR', 'TXSQL'])

        else:

            AllService = {'TOS', 'LICENSE_SERVICE', 'ZOOKEEPER', 'CODIS', 'HDFS', 'YARN', 'HYPERBASE', 'TXSQL', 'SEARCH',
                          'GUARDIAN', 'INCEPTOR', 'TRANSPORTER', 'KAFKA', 'PILOT', 'WORKFLOW', 'NOTIFICATION', 'RUBIK','SHIVA'}
            AllServiceLength = len(AllService)
            prerequisites.append(['LICENSE_SERVICE', 'TOS'])
            prerequisites.append(['ZOOKEEPER', 'LICENSE_SERVICE'])
            prerequisites.append(['HDFS', 'ZOOKEEPER'])
            prerequisites.append(['YARN', 'HDFS'])
            prerequisites.append(['SEARCH', 'YARN'])
            prerequisites.append(['HYPERBASE', 'SEARCH'])
            prerequisites.append(['TXSQL', 'HDFS'])
            prerequisites.append(['GUARDIAN', 'TXSQL'])
            prerequisites.append(['INCEPTOR', 'HYPERBASE'])
            prerequisites.append(['INCEPTOR', 'GUARDIAN'])
            prerequisites.append(['CODIS', 'INCEPTOR'])
            prerequisites.append(['KAFKA', 'ZOOKEEPER'])
            prerequisites.append(['TRANSPORTER', 'KAFKA'])
            prerequisites.append(['TRANSPORTER', 'INCEPTOR'])
            prerequisites.append(['PILOT', 'INCEPTOR'])
            prerequisites.append(['NOTIFICATION', 'INCEPTOR'])
            prerequisites.append(['WORKFLOW', 'INCEPTOR'])
            prerequisites.append(['RUBIK', 'NOTIFICATION'])
            prerequisites.append(['RUBIK', 'WORKFLOW'])
            prerequisites.append(['SHIVA', 'INCEPTOR'])

        edges = {i: [] for i in AllService}
        degrees = dict.fromkeys(AllService, 0)

        for i, j in prerequisites:
            edges[j].append(i)
            degrees[i] += 1

        import Queue
        import copy
        q = Queue.Queue(maxsize=AllServiceLength)

        for i in AllService:
            if degrees[i] == 0:
                q.put(i)

        order = []
        while not q.empty():
            node = q.get()
            order.append(node)
            if node in service_install_list:
                service_lists.append(copy.deepcopy(order))
            for x in edges[node]:
                degrees[x] -= 1
                if degrees[x] == 0:
                    if x not in service_install_list and len(edges[x]) == 0 and len(edges[node]) == 1:
                        order.remove(node)
                    if x not in service_install_list and len(edges[x]) == 0:
                        continue
                    q.put(x)
        """
        if len(order) == AllServiceLength:
            return service_lists
        """
        # get union, service_lists [[zookeeper], [zookeeper, hdfs], [zookeeper, hdfs, yarn]]

        result = []
        for item in service_lists:
            # result = list(set(result).union(set(item)))
            if not result:
                result = item[:]
            else:
                for i in range(len(item)):
                    if item[i] in result:
                        continue
                    else:
                        pos = result.index(item[i - 1])
                        result.insert(pos + 1, item[i])
        for service in service_install_list:
            if not service in result:
                result.append(service)
        print(result)
        return ",".join(result)


    @classmethod
    def send_email(cls, params):
        # coding=utf-8
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        fromaddr = "jenkins@transwarp.io"
        toaddr = str(params.get("email"))
        username = "jenkins@transwarp.io"
        password = "Or37aZ0ST7WV0fBj"
        tdh_version = params.get("tdh_version")
        nodes = params.get("nodes")
        # judge whether subtask exists
        table_params = []
        resource_type = "Node"
        if nodes[0]['hostname'].strip():
            resource_type = "Service"

        manager_ip = nodes[0]['float_ip']
        if resource_type == "Node":
            manager_ip = ""

        for node in nodes:
            table_param = cls.generate_tr(node['name'], node['hostname'], node['inner_ip'], node['float_ip'], node['username'], node['password'])
            table_params.append(table_param)

        table_params = '\n'.join(table_params)

        # define msg header
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "[CMS-Link]Congratulations, Your task succeed!"
        msg['From'] = fromaddr
        tolist = [x.strip() for x in toaddr.split(',')]
        if 'youzhi.su@transwarp.io' not in tolist:
            tolist.append('youzhi.su@transwarp.io')

        msg['To'] = ",".join(tolist)

        text = "Hi!\nHere is information about Cms-celery task\n"

        # define msg body
        html = """\
        <!doctype html>
        <html>
          <head>
            <meta name="viewport" content="width=device-width">
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>Simple Transactional Email</title>
            <style>
            /* -------------------------------------
                INLINED WITH htmlemail.io/inline
            ------------------------------------- */
            /* -------------------------------------
                RESPONSIVE AND MOBILE FRIENDLY STYLES
            ------------------------------------- */
            @media only screen and (max-width: 620px) {{
              table[class=body] h1 {{
                font-size: 28px !important;
                margin-bottom: 10px !important;
              }}
              table[class=body] p,
                    table[class=body] ul,
                    table[class=body] ol,
                    table[class=body] td,
                    table[class=body] span,
                    table[class=body] a {{
                font-size: 16px !important;
              }}
              table[class=body] .wrapper,
                    table[class=body] .article {{
                padding: 10px !important;
              }}
              table[class=body] .content {{
                padding: 0 !important;
              }}
              table[class=body] .container {{
                padding: 0 !important;
                width: 100% !important;
              }}
              table[class=body] .main {{
                border-left-width: 0 !important;
                border-radius: 0 !important;
                border-right-width: 0 !important;
              }}
              table[class=body] .btn table {{
                width: 100% !important;
              }}
              table[class=body] .btn a {{
                width: 100% !important;
              }}
              table[class=body] .img-responsive {{
                height: auto !important;
                max-width: 100% !important;
                width: auto !important;
              }}
            }}
            /* -------------------------------------
                PRESERVE THESE STYLES IN THE HEAD
            ------------------------------------- */
            @media all {{
              .ExternalClass {{
                width: 100%;
              }}
              .ExternalClass,
                    .ExternalClass p,
                    .ExternalClass span,
                    .ExternalClass font,
                    .ExternalClass td,
                    .ExternalClass div {{
                line-height: 100%;
              }}
              .apple-link a {{
                color: inherit !important;
                font-family: inherit !important;
                font-size: inherit !important;
                font-weight: inherit !important;
                line-height: inherit !important;
                text-decoration: none !important;
              }}
              .btn-primary table td:hover {{
                background-color: #34495e !important;
              }}
              .btn-primary a:hover {{
                background-color: #34495e !important;
                border-color: #34495e !important;
              }}
            }}
            </style>
          </head>
          <body class="" style="background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;">
              <tr>
                <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>
                <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; Margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;">
                  <div class="content" style="box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;">

                    <!-- START CENTERED WHITE CONTAINER -->
                    <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">Congratulations!!! Your task complete succeed, click on me to see more information</span>
                    <table class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background: #ffffff; border-radius: 3px;">

                      <!-- START MAIN CONTENT AREA -->
                      <tr>
                        <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;">
                          <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                            <tr>
                              <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;"><b>[Cms Cluster Install]</b><br>Resource Type: {resource_type_text} succeed!</p>
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;"><b>Manager IP: {manager_ip_text}</b></p>
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;"><b>TDH Version: {tdh_version_text}</b></p>
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">
                                  <table border="1">
                                    <tr><th>Name</th><th>Hostname</th><th>Inner_ip</th><th>Float_ip</th><th>Username</th><th>Password</th></tr>
                                    {param_tds}
                                  </table>
                                </p>

                                <table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; box-sizing: border-box;">
                                  <tbody>
                                    <tr>
                                      <td align="left" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;">
                                        <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: auto;">
                                          <tbody>
                                            <tr>
                                              <td style="font-family: sans-serif; font-size: 14px; vertical-align: top; background-color: #3498db; border-radius: 5px; text-align: center;"> <a href="mailto:zhiyang.dai@transwarp.io" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db;">Call To Action</a> </td>
                                            </tr>
                                          </tbody>
                                        </table>
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">Click <a href="http://172.16.1.76"><b>Here</b></a> to log in openstack</p>
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">Good luck! Hope it works.</p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>

            <!-- END MAIN CONTENT AREA -->
            </table>
                    <div class="footer" style="clear: both; Margin-top: 10px; text-align: center; width: 100%;">
                      <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                        <tr>
                          <td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                            <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">Transwarp</span>
                            <br>Call me to ask more information<a href="https://skydai.github.io" style="text-decoration: underline; color: #999999; font-size: 12px; text-align: center;"><b>GateWay</b></a>.
                          </td>
                        </tr>
                        <tr>
                          <td class="content-block powered-by" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                            Powered by <a href="https://skydai.github.io" style="color: #999999; font-size: 12px; text-align: center; text-decoration: none;">zhiyang.dai</a>.
                          </td>
                        </tr>
                      </table>
                    </div>

                  </div>
                </td>
                <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>
              </tr>
            </table>
          </body>
        </html>
        """
        # retval task_id args kwargs

        html = html.format(resource_type_text=resource_type, manager_ip_text=manager_ip, tdh_version_text=tdh_version, param_tds=table_params)
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # attach parts into msg container
        msg.attach(part1)
        msg.attach(part2)

        try:
            server = smtplib.SMTP_SSL('smtp.exmail.qq.com', port=465)
            # open debug and print logs
            # server.set_debuglevel(1)
            print("--- Need Authentication ---")
            server.login(username, password)
            server.sendmail(fromaddr, tolist, msg.as_string())
            print("success")
        except Exception as e:
            tolist = ['youzhi.su@transwarp.io']
            server.sendmail(fromaddr, tolist, msg.as_string())
            logger.warn('Exception: send user email: ' + str(toaddr) + ' failed, Forward email to admin now: ' + str(e))

        server.quit()


    @classmethod
    def generate_tr(cls, name, hostname, inner_ip, float_ip, username, password):
        return '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (name, hostname, inner_ip, float_ip, username, password)

    @classmethod
    def call_back(cls, params):

        status = "RUNNING"
        nodes = params.get('nodes')
        try:
            HttpClientUtil.doPut(url=str(UPDATE_OPENSTACK_NODE), auth_token="",
                                 data=json.dumps({"nodes": nodes, "status": status}))
        except Exception as e:
            logger.warn("PUT:  " + str(UPDATE_OPENSTACK_NODE) + " --data " + str(json.dumps({"nodes": nodes})) + " FAIL")

        return params


