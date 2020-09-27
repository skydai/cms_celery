FROM 172.16.1.99/lisong/cms:base

MAINTAINER lisong.qiu@transwarp.io

#RUN echo "nameserver 114.114.114.114" >/etc/resolv.conf && yum clean all && yum install -y wget  gcc gcc-c++ c++ c make && yum clean all
RUN pip install -i  http://172.16.1.161:30033/repository/pypi/simple --trusted-host 172.16.1.161 libappadapter tdc_commons kts-gen

USER root
ADD . /root
ADD product-meta.tar.gz /root
ENV PRODUCT_META_HOME /root/product-meta
ENV BROKER_URL redis://172.16.1.161:30908/
ENV CELERY_RESULT_BACKEND db+mysql://root:transwarp@172.16.130.96:30637/cms_celery
EXPOSE 5000 5555