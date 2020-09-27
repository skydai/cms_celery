#!/bin/bash

basedir=$(cd `dirname $0`; pwd)

tdh_version=$1
[ "${tdh_version}" == "" ] && echo "tdh_version is null ...." && exit 1

tdh_ui_web_install_addr="http://lisong:transwarp@172.16.1.41:10080/InfraTools/tdh_ui_web_install.git"

cd /tmp

echo "nameserver 114.114.114.114" >/etc/resolv.conf
echo "172.16.1.168 transwarp" >>/etc/hosts

sleep 30s

flag="false"
for i in `seq 1 10`
do
    yum install -y git
    [ $? -eq 0 ] && flag="true" && break
    sleep 30s

done

if [ "${flag}" == "false" ];then
     echo "yum install git fail..."
     exit 1
fi

if [[ ${tdh_version} =~ "transwarp-ce-1.1" ]]; then
    TDHAutoInstallTarLoc="http://172.16.1.97:8080/remote.php/webdav/TDHAutoInstall/ce-1.1/TDHAutoInstall.tar.gz"
elif [[ ${tdh_version} =~ "transwarp-4" ]]; then
    TDHAutoInstallTarLoc="http://172.16.1.97:8080/remote.php/webdav/TDHAutoInstall/4.x/TDHAutoInstall.tar.gz"
elif [[ ${tdh_version} =~ "transwarp-6" ]]; then
    TDHAutoInstallTarLoc="http://172.16.1.97:8080/remote.php/webdav/TDHAutoInstall/6.x/TDHAutoInstall.tar.gz"
else
    TDHAutoInstallTarLoc="http://172.16.1.97:8080/remote.php/webdav/TDHAutoInstall/5.x/TDHAutoInstall.tar.gz"
fi

[ -e auto_web_install ] && rm -rf auto_web_install

if [[ ${tdh_version} =~ "transwarp-ce" ]]; then
     echo "tdh version include transwarp-ce"
     git clone -b transwarp-ce-dev ${tdh_ui_web_install_addr} auto_web_install

elif [[ ${tdh_version} =~ "transwarp-5.0" ]]; then
     echo "tdh version include transwarp-5.0"
     git clone -b transwarp-5.0-dev ${tdh_ui_web_install_addr} auto_web_install

elif [[ ${tdh_version} =~ "transwarp-5.1" ]]; then
    echo "tdh version include transwarp-5.1"
    git clone -b  transwarp-5.1-dev  ${tdh_ui_web_install_addr} auto_web_install

elif [[ ${tdh_version} =~ "transwarp-5.2" ]]; then
    echo "tdh version include transwarp-5.2"
    git clone -b transwarp-5.2-dev ${tdh_ui_web_install_addr} auto_web_install

elif [[ ${tdh_version} =~ "transwarp-6.0" ]]; then
    echo "tdh version include transwarp-6.0"
    git clone -b transwarp-6.0-dev ${tdh_ui_web_install_addr} auto_web_install

elif [[ ${tdh_version} =~ "transwarp-6.1" ]]; then
    echo "tdh version include transwarp-6.1"
    git clone -b transwarp-6.1-dev ${tdh_ui_web_install_addr} auto_web_install

elif [[ ${tdh_version} =~ "sophon" ]]; then
    echo "tdh version include sophon"
    git clone -b sophon-dev ${tdh_ui_web_install_addr} auto_web_install

elif [[ ${tdh_version} =~ "transwarp-4" ]]; then
    echo "tdh version ${tdh_version}"
    git clone -b transwarp-4.9-dev ${tdh_ui_web_install_addr} auto_web_install

else
     echo "${tdh_version} is not support.... only support transwarp-ce/transwarp-5.1/transwarp-5.0/transwarp-5.2"
     exit 1
fi

echo "git clone suc"

echo "copy TDHAutoInstall.tar.gz"
cd /opt
curl -u qa:123456 -O ${TDHAutoInstallTarLoc}

exit 0
