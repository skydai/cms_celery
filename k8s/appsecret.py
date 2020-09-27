# -*- coding: utf-8 -*-

import sys
sys.path.append('./..')
from .k8sconfig import Settings

from secretgen.configuration import secretgen_configuration
from secretgen.gen import generate_keytab_secret

HARBOR_BASE_URL = Settings.HARBOR_BASE_URL
LICENSE_ADDRESS = Settings.LICENSE_ADDRESS
KDC_SERVER_ADDRESS = Settings.KDC_SERVER_ADDRESS

secretgen_configuration.guardian_server_address = Settings.GUARDIAN_SERVER_ADDRESS
secretgen_configuration.guardian_admin_username = Settings.GUARDIAN_ADMIN_USERNAME
secretgen_configuration.guardian_admin_password = Settings.GUARDIAN_ADMIN_PASSWORD


class K8sAppSecret(object):

    @classmethod
    def create_service_secret(cls, service_name, tenant_name, principal_list, secret_name):

        labels = {
            'transwarp.keytab': secret_name
        }
        annotations = {
            'kubernetes.io/service-account.name': 'default'
        }

        secret = generate_keytab_secret(principal_list=principal_list,
                                        generate_name=secret_name,
                                        labels=labels,
                                        annotations=annotations,
                                        extra_krb_configs={
                                            'kdc_addresses': [
                                                KDC_SERVER_ADDRESS
                                            ],
                                            'realm': 'TDH'
                                        })

        return secret