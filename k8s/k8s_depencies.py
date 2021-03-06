# coding:utf-8
import copy
import logging

logger = logging.getLogger(__name__)


class K8sDependencies(object):

    @classmethod
    def get_dependencies(cls, tdh_version, install_list):
            # contruct prerequisites
            # [0, 1] to install 0, you must install 1 first
            # eg: service_install_list zookeeper, hdfs, yarn
            # GUARDIAN
        service_install_list = install_list.split(',')
        prerequisites = []
        service_lists = []

        AllService = {'HDFS', 'YARN', 'HYPERBASE', 'TXSQL', 'SEARCH', 'INCEPTOR', 'SOPHON'}
        AllServiceLength = len(AllService)

        prerequisites.append(['YARN', 'HDFS'])
        prerequisites.append(['SEARCH', 'YARN'])
        prerequisites.append(['HYPERBASE', 'SEARCH'])
        prerequisites.append(['TXSQL', 'HDFS'])
        prerequisites.append(['INCEPTOR', 'TXSQL'])
        prerequisites.append(['SOPHON', 'INCEPTOR'])

        # if str(tdh_version).startswith('transwarp-5.2') or str(tdh_version).startswith('transwarp-5.1'):
        #     prerequisites.append(['YARN', 'HDFS'])
        #     prerequisites.append(['SEARCH', 'YARN'])
        #     prerequisites.append(['HYPERBASE', 'SEARCH'])
        #     prerequisites.append(['TXSQL', 'HDFS'])
        #     prerequisites.append(['INCEPTOR', 'TXSQL'])
        #     prerequisites.append(['SOPHON', 'INCEPTOR'])
        #
        # else:
        #     raise Exception("only support transwarp-5.1/transwarp-5.2 k8s install")

        edges = {i: [] for i in AllService}
        degrees = dict.fromkeys(AllService, 0)

        for i, j in prerequisites:
            edges[j].append(i)
            degrees[i] += 1

        import Queue
        q = Queue.Queue(maxsize=AllServiceLength)

        for i in AllService:
            if degrees[i] == 0:
                q.put(i)

        order = []
        while not q.empty():
            node = q.get()
            order.append(node)
            if node in service_install_list:
                order_copy = copy.deepcopy(order)
                service_lists.append(order_copy)
            for x in edges[node]:
                degrees[x] -= 1
                if degrees[x] == 0:
                    if not x in service_install_list and len(edges[x]) == 0 and len(edges[node]) == 1:
                        order.remove(node)
                    if not x in service_install_list and len(edges[x]) == 0:
                        continue
                    q.put(x)
            """
            if len(order) == AllServiceLength:
                return service_lists
            """

        result = []
        for item in service_lists:
            if not result:
                result = item[:]
            else:
                for i in range(len(item)):
                    if item[i] in result:
                        continue
                    else:
                        pos = result.index(item[i-1])
                        result.insert(pos+1, item[i])
        for service in service_install_list:
            if not service in result:
                result.append(service)

        return result
