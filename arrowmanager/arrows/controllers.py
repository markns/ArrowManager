import os

from kubernetes import client, config

# TODO: Would be nice to create a Flask-Kube extension
from arrowmanager import models

config.load_kube_config(os.environ["HOME"] + '/.kube/config')
k8s = client.CoreV1Api()


def get_pod_status(tenant):
    # TODO: use this k8s.list_namespaced_pod()
    # pods = k8s.list_pod_for_all_namespaces()
    pods = k8s.list_namespaced_pod(namespace=tenant)
    return pods


def get_applications(tenant):
    try:
        query = {'tenant': tenant}
        result = models.Application.objects(**query)
        return result
    except Exception as e:
        return {'error': 'Error during the operation: {}'.format(e)}
