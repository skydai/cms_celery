#!/usr/bin/env bash

export PRODUCT_META_HOME=/root/product-meta
nohup celery flower -A cms_celery --broker=redis://172.16.1.161:30908 &
celery multi start w1 -A cms_celery -l info -c 3
celery multi start w2 -A cms_celery -l info -c 3
celery multi start w3 -A cms_celery -l info -c 3
celery multi start w4 -A cms_celery -l info -c 3
celery multi start w5 -A cms_celery -l info -c 3
celery multi start w6 -A cms_celery -l info -c 3
celery multi start w7 -A cms_celery -l info -c 3
celery multi start w8 -A cms_celery -l info -c 3

python cms_celery.py runserver -h 0.0.0.0