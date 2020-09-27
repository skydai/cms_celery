#!/bin/bash
# Create and publish Ockle image
set -e

basedir=$(cd `dirname $0`; pwd)
PUB_TAG=172.16.1.99/postcommit/cms-celery:argon-1.0

docker build -t ${PUB_TAG} .

docker push $PUB_TAG

echo "Success!"
