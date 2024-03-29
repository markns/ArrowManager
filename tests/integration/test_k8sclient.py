import os
import uuid

import pytest
import urllib3
from kubernetes import config, client


def _k8s_endpoint():
    config.load_kube_config(os.environ["HOME"] + '/.kube/config')
    c = client.Configuration()
    return c.host


def _k8s_not_running():
    try:
        urllib3.disable_warnings()
        urllib3.PoolManager().request('GET', _k8s_endpoint())
        return False
    except urllib3.exceptions.HTTPError:
        return True


class TestK8sclient:
    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_list_endpoints(self, k8s: client.CoreV1Api):
        endpoints = k8s.list_endpoints_for_all_namespaces()
        assert len(endpoints.items) > 0

    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_deployment_apis(self, k8s: client.ExtensionsV1beta1Api):
        # k8s.create_namespaced_deployment()
        pass

    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_pod_apis(self, k8s: client.CoreV1Api):
        name = 'test-' + str(uuid.uuid4())

        pod_manifest = {'apiVersion': 'v1',
                        'kind': 'Pod',
                        'metadata': {'color': 'blue', 'name': name},
                        'spec': {'containers': [{'image': 'alpine',
                                                 'name': 'test'}]}}

        resp = k8s.create_namespaced_pod(body=pod_manifest,
                                         namespace='default')
        assert name == resp.metadata.name
        assert resp.status.phase == 'Pending'

        resp = k8s.read_namespaced_pod(name=name,
                                       namespace='default')
        assert name == resp.metadata.name
        assert resp.status.phase == 'Pending'

        number_of_pods = len(k8s.list_pod_for_all_namespaces().items)
        assert number_of_pods > 0
        # resp = k8s.delete_namespaced_pod(name=name, body={},
        #                                  namespace='default')

    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_service_apis(self, k8s: client.ExtensionsV1beta1Api):
        name = 'test-' + str(uuid.uuid4())

        service_manifest = {'apiVersion': 'v1',
                            'kind': 'Service',
                            'metadata': {'labels': {'name': name},
                                         'name': name,
                                         'resourceversion': 'v1'},
                            'spec': {'ports': [{'name': 'port',
                                                'port': 80,
                                                'protocol': 'TCP',
                                                'targetPort': 80}],
                                     'selector': {'name': name}}}

        resp = k8s.create_namespaced_service(body=service_manifest,
                                             namespace='default')
        assert name == resp.metadata.name
        # assert resp.status == 'Pending'

        resp = k8s.read_namespaced_service(name=name,
                                           namespace='default')
        assert name == resp.metadata.name
        # assert resp.status is True

        # service_manifest['spec']['ports'] = [{'name': 'new',
        #                                       'port': 8080,
        #                                       'protocol': 'TCP',
        #                                       'targetPort': 8080}]
        # resp = k8s.patch_namespaced_service(body=service_manifest,
        #                                     name=name,
        #                                     namespace='default')
        # assert 2 == len(resp.spec.ports)
        # assert resp.status is True

        resp = k8s.delete_namespaced_service(name=name,
                                             namespace='default')

    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_replication_controller_apis(self, k8s: client.CoreV1Api):
        name = 'test-' + str(uuid.uuid4())

        rc_manifest = {
            'apiVersion': 'v1',
            'kind': 'ReplicationController',
            'metadata': {'labels': {'name': name},
                         'name': name},
            'spec': {'replicas': 2,
                     'selector': {'name': name},
                     'template': {'metadata': {
                         'labels': {'name': name}},
                         'spec': {'containers': [{
                             'image': 'nginx',
                             'name': 'nginx',
                             'ports': [{'containerPort': 80,
                                        'protocol': 'TCP'}]}]}}}}

        resp = k8s.create_namespaced_replication_controller(
            body=rc_manifest, namespace='default')
        assert name == resp.metadata.name
        assert 2 == resp.spec.replicas

        resp = k8s.read_namespaced_replication_controller(
            name=name, namespace='default')
        assert name == resp.metadata.name
        assert 2 == resp.spec.replicas

        resp = k8s.delete_namespaced_replication_controller(
            name=name, body={}, namespace='default')

    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_configmap_apis(self, k8s: client.CoreV1Api):
        name = 'test-' + str(uuid.uuid4())
        test_configmap = {
            "kind": "ConfigMap",
            "apiVersion": "v1",
            "metadata": {
                "name": name,
            },
            "data": {
                "config.json": "{\"command\":\"/usr/bin/mysqld_safe\"}",
                "frontend.cnf": "[mysqld]\nbind-address = 10.0.0.3\nport = 3306\n"
            }
        }

        resp = k8s.create_namespaced_config_map(
            body=test_configmap, namespace='default'
        )
        assert name == resp.metadata.name

        resp = k8s.read_namespaced_config_map(
            name=name, namespace='default')
        assert name == resp.metadata.name

        # test_configmap['data']['config.json'] = "{}"
        # resp = k8s.patch_namespaced_config_map(
        #     name=name, namespace='default', body=test_configmap)

        resp = k8s.delete_namespaced_config_map(
            name=name, body={}, namespace='default')

    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_node_apis(self, k8s: client.CoreV1Api):
        for item in k8s.list_node().items:
            node = k8s.read_node(name=item.metadata.name)
            # assert len(node.metadata.labels) > 0
            # assert isinstance(node.metadata.labels, dict) is True

    @pytest.mark.skipif(_k8s_not_running(), reason="Kubernetes is not available")
    def test_ingress_apis(self, k8s: client.ExtensionsV1beta1Api):
        # k8s.patch_namespaced_ingress_status_with_http_info()
        pass
            # node = k8s.read_node(name=item.metadata.name)
            # assert len(node.metadata.labels) > 0
            # assert isinstance(node.metadata.labels, dict) is True


# class TestK8sclientBeta(base.TestCase):
#     @pytest.mark.skipif(
#         _is_k8s_running(), reason="Kubernetes is not available")
#     def test_deployment_apis(self):
#         client = k8s_client.k8sClient(K8S_ENDPOINT)
#         k8s = k8ssextensionsvbeta_k8s.k8ssextensionsvbetak8s(client)
# 
#         deployment_manifest = {
#             'kind': 'Deployment',
#             'spec': {
#                 'template':
#                     {'spec':
#                       {'containers': [
#                             {'image': 'nginx',
#                              'name': 'test-deployment',
#                              'ports': [{'containerPort': 80}]
#                              }
#                         ]},
#                         'metadata': {'labels': {'app': 'test-deployment'}}},
#                 'replicas': 2},
#             'apiVersion': 'extensions/v1beta1',
#             'metadata': {'name': 'test-deployment'}}
# 
#         resp = k8s.create_namespaced_deployment(
#             body=deployment_manifest, namespace='default')
#         assert 'test-deployment', resp.metadata.name)
#         assert 2, resp.spec.replicas)
# 
#         resp = k8s.read_namespaced_deployment(
#             name='test-deployment', namespace='default')
#         assert 'test-deployment', resp.metadata.name)
#         assert 2, resp.spec.replicas)
# 
#         deployment_manifest['spec']['replicas'] = 1
#         resp = k8s.patch_namespaced_deployment(
#             name='test-deployment', namespace='default',
#             body=deployment_manifest)
#         assert 1, resp.spec.replicas)
# 
#         resp = k8s.delete_namespaced_deployment(
#             name='test-deployment', body={}, namespace='default')
