# OpenSearch Deployment

## Fix the WSL2 Memory Limit (If running on Windows)
    $ wsl -d docker-desktop sysctl -w vm.max_map_count=262144

## Install OpenSearch Docker locally
    $ docker run --name elasticsearch -d -p 9200:9200 -e "cluster.name=docker-cluster" -e "node.name=opensearch-node1" -e "cluster.initial_master_nodes=opensearch-node1" -e "plugins.security.disabled=true" -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" opensearchproject/opensearch:1.3.16

## .env file on your local
    OPENSEARCH_URL=localhost
    OPENSEARCH_PORT=9200
    OPENSEARCH_USE_SSL=False
    OPENSEARCH_VERIFY_CERTS=False
    OPENSEARCH_SERVICE=

## Reindex the Post table
    $ source venv/bin/activate
    (venv) $ flask shell
    >>> from app.models import Post
    >>> Post.reindex()
    >>> exit()