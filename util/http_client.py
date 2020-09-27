# coding:utf-8
import json
import logging

import requests

logger = logging.getLogger(__name__)


class HttpClientUtil(object):
    @staticmethod
    def doPost(url, data, auth_token=""):

        if auth_token != "":
            headers = {'content-type': 'application/json',
                       'x-auth-token': auth_token}
        else:
            headers = {'content-type': 'application/json'}

        logger.info("HEADERS: " + str(headers))
        logger.info("POST:  " + url + " --data " + data)

        try:

            result = requests.post(url=url, data=data, headers=headers, timeout=60)
            logger.info("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            raise Exception(str(result.text))

        return result

    @staticmethod
    def doGet(url, auth_token, **kwargs):

        headers = {'content-type': 'application/json',
                   'x-auth-token': auth_token}

        logger.info("HEADERS: " + str(headers))
        logger.info("GET:  " + url + " --data " + str(kwargs))

        try:

            result = requests.get(url=url, headers=headers, timeout=60, **kwargs)
            logger.info("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            raise Exception(str(result.text))

        return result


    @staticmethod
    def doPut(url, auth_token, data, **kwargs):

        if auth_token == "":
            headers = {'content-type': 'application/json'}
        else:
            headers = {'content-type': 'application/json',
                       'x-auth-token': auth_token}

        logger.info("HEADERS: " + str(headers))
        logger.info("PUT:  " + url + " --data " + str(data))

        try:

            result = requests.put(url=url, headers=headers, data=data, timeout=60, **kwargs)
            logger.info("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            raise Exception(str(result.text))

        return result


    @staticmethod
    def doDelete(url, auth_token, **kwargs):

        headers = {'content-type': 'application/json',
                   'x-auth-token': auth_token}

        logger.info("HEADERS: " + str(headers))
        logger.info("DELETE:  " + url + " --data " + str(kwargs))

        try:

            result = requests.delete(url=url, headers=headers, timeout=60, **kwargs)
            logger.info("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            raise Exception(str(result.text))

        return result


if __name__ == '__main__':
    url = "http://172.16.130.78:5000/v2.0/tokens"
    data = {
        "auth": {
            "tenantName": "admin",
            "passwordCredentials": {
                "username": "admin",
                "password": "admin"
            }
        }
    }

    result = HttpClientUtil.doPost(url, json.dumps(data))
    print json.loads(result.text)['access']['token']['id']
