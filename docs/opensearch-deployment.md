# OpenSearch Deployment

## Install OpenSearch Docker locally
    docker run --name elasticsearch -d --rm -p 9200:9200 -e discovery.type=single-node -e plugins.security.disabled=true -e "DISABLE_SECURITY_PLUGIN=true" opensearchproject/opensearch:1.3.16