from pip import main as pipmain

pipmain(['install', "-q", "dask_kubernetes"])

import ssl
import urllib.request
import yaml
from dask_kubernetes import KubeCluster
import distributed

cluster_node = 5
adapt_min = 1
adapt_max = 10
limits_cpu = 2
limits_memory = 4
requests_cpu = 1
requests_memory = 2

def spinupCluster(cluster_node = cluster_node, adapt_min = adapt_min, adapt_max = adapt_max, limits_cpu = limits_cpu, limits_memory = limits_memory, requests_cpu = requests_cpu, requests_memory = requests_memory):
    assert cluster_node in range(1, 41), "Number of nodes out of bound."
    assert adapt_min in range(1, 41), "Adaptive minimum number of nodes out of bound."
    assert adapt_max in range(1, 41), "Adaptive maximum number of nodes out of bound."
    assert limits_cpu > 0 and limits_cpu <= 2, "CPU limits out of bound."
    assert limits_memory > 0 and limits_memory <= 6, "Memory limits out of bound."
    assert requests_cpu > 0 and requests_cpu <= 1, "CPU requests out of bound."
    assert requests_memory > 0 and requests_memory <= 2, "Memory requests out of bound."
    
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "http://gitlab.devkubewd.dev.blackrock.com/mdiao/aladdin-dask-cluster/raw/master/worker-spec.yml"
    with urllib.request.urlopen(url) as x:
        worker_spec = x.read()
    worker_spec_dic = yaml.load(worker_spec)
    
    worker_spec_dic['spec']['containers'][0]['resources']['limits']['cpu'] = str(limits_cpu)
    worker_spec_dic['spec']['containers'][0]['resources']['limits']['memory'] = str(limits_memory) + 'G'
    worker_spec_dic['spec']['containers'][0]['resources']['requests']['cpu'] = str(requests_cpu)
    worker_spec_dic['spec']['containers'][0]['resources']['requests']['memory'] = str(requests_memory) + 'G'
    
    cluster = KubeCluster.from_dict(worker_spec_dic)
    
    cluster.scale_up(cluster_node)
    cluster.adapt(minimum = adapt_min, maximum = adapt_max)
    
    client = distributed.Client(cluster)
    
    return client