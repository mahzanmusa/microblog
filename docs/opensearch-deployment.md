# OpenSearch Deployment

## Install OpenSearch Docker locally
    docker run --name elasticsearch -d --rm -p 9200:9200 -e "discovery.type=single-node" -e "cluster.name=docker-cluster" -e "node.name=os-node" -e "cluster.initial_master_nodes=os-node" -e "plugins.security.disabled=true" -e "DISABLE_SECURITY_PLUGIN=true" opensearchproject/opensearch:1.3.16