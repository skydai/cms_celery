# coding:utf-8
import logging
import os
import random
import smtplib
import time
import traceback
from email.header import Header
from email.mime.text import MIMEText

import paramiko

logger = logging.getLogger(__name__)

class TdhClusterUtil(object):

    @staticmethod
    def get_project_path():
        base_dir = os.path.dirname(os.path.dirname(__file__))
        base_dir = str(base_dir)
        base_dir = base_dir.replace('\\', '/')
        return base_dir


    @staticmethod
    def get_now_time(format="%Y-%m-%d_%H-%M-%S"):
        return time.strftime(format)

    @staticmethod
    def readlines(file):
        lines = []
        try:
            f = open(file, 'r')
            lines = f.readlines()
        except IOError:
            print 'error occurs while reading file'
        finally:
            f.close()
        return lines

    @staticmethod
    def readline(file):
        try:
            f = open(file, 'r')
            while True:
                line = f.readline()
                if line:
                    print "line: " + str(line)
                else:
                    break
        except IOError:
            print 'error occurs while reading file'
        finally:
            f.close()

    @staticmethod
    def send_email(file_new):
        f = open(file_new, 'rb')
        mail_body = f.read()
        f.close()

        msg = MIMEText(mail_body, 'html', 'utf-8')
        msg['Subject'] = Header("Test Report", 'utf-8')

        smtp = smtplib.SMTP()
        smtp.connect("smtp.exmail.qq.com")
        smtp.login("prod@transwarp.io", "Warp1234")
        smtp.sendmail("prod@transwarp.io", "youzhi.su@transwarp.io", msg.as_string())
        smtp.quit()

    @staticmethod
    def lastest_report():
        report_dir = TdhClusterUtil.get_project_path()+"/report/logs/"
        lists = os.listdir(report_dir)
        lists.sort(key=lambda fn: os.path.getmtime(report_dir + "/" + fn))
        file_new = os.path.join(report_dir, lists[-1])
        return file_new


    @staticmethod
    def GetFileList(dir, fileList):
        '''
        :param dir:
        :param fileList:
        :return: fileList
        :eg： list = TdhClusterUtil.GetFileList('/tmp', [])
        '''
        newDir = dir
        if os.path.isfile(dir):
            fileList.append(dir.decode('utf-8'))
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                #如果需要忽略某些文件夹，使用以下代码
                #if s == "xxx":
                    #continue
                newDir = os.path.join(dir, s)
                TdhClusterUtil.GetFileList(newDir, fileList)
        return fileList

    @staticmethod
    def random_int(a, b):
        """Return random integer in range [a, b], including both end points.
        """
        return random.randint(a, b)

    @staticmethod
    def exec_remote_script(hostname, username, password, shell_script):
        try:
            # paramiko.util.log_to_file('/tmp/paramiko.log')
            s = paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.load_system_host_keys()
            s.connect(hostname=hostname, username=username, password=password)
            chan = s.get_transport().open_session()
            chan.exec_command(shell_script)

            exit_code = chan.recv_exit_status()
            s.close()

            return exit_code
        except Exception, e:
            logger.error(e)
            logger.error('traceback.format_exc(): %s' % traceback.format_exc())
            raise

    @staticmethod
    def scp_file_to_remote(hostname, username, password, local_file, remote_file, port=22):
        try:
            # 建立一个加密的管道
            scp = paramiko.Transport((hostname, port))

            # 建立连接
            scp.connect(username=username, password=password)
            # 建立一个sftp客户端对象，通过ssh transport操作远程文件
            sftp = paramiko.SFTPClient.from_transport(scp)

            # Copy a remote file (remotepath) from the SFTP server to the local host
            # sftp.get(remote_file, local_file)

            # Copy a local file (localpath) to the SFTP server as remotepath
            sftp.put(local_file, remote_file)
            scp.close()
            return True
        except Exception, e:
            logger.error(e.message)
            return False

    @staticmethod
    def scp_remote_file_to_local(hostname, username, password, remote_file, local_file, port=22):
        try:
            # 建立一个加密的管道
            scp = paramiko.Transport((hostname, port))
            # 建立连接
            scp.connect(username=username, password=password)
            # 建立一个sftp客户端对象，通过ssh transport操作远程文件
            sftp = paramiko.SFTPClient.from_transport(scp)

            # Copy a remote file (remotepath) from the SFTP server to the local host
            sftp.get(remote_file, local_file)
            scp.close()
            return True
        except Exception, e:
            print e
            return False

    @staticmethod
    def scp_remote_dir_to_local(hostname, username, password, remote_dir, local_dir, port=22):

        try:

            # 建立一个加密的管道
            scp = paramiko.Transport((hostname, port))
            # 建立连接
            scp.connect(username=username, password=password)
            # 建立一个sftp客户端对象，通过ssh transport操作远程文件
            sftp = paramiko.SFTPClient.from_transport(scp)

            # 保存所有文件的列表
            all_files = list()

            # 去掉路径字符串最后的字符'/'，如果有的话
            if remote_dir[-1] == '/':
                remote_dir = remote_dir[0:-1]

            # 获取当前指定目录下的所有目录及文件，包含属性值
            files = sftp.listdir_attr(remote_dir)
            for x in files:
                # remote_dir目录中每一个文件或目录的完整路径
                filename = remote_dir + '/' + x.filename
                local_filename = os.path.join(local_dir, x.filename)
                sftp.get(filename, local_filename)

            scp.close()
            return True

        except Exception, e:
            print e
            return False

if __name__ == '__main__':
    print str(TdhClusterUtil.get_project_path() + "/scripts/")
