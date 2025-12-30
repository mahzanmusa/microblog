# Microblog Deployment - Docker Container

## Create the Network (if not already)
    $ docker network create microblog-network

## Build
    $ cd microblog
    $ docker build -t microblog:latest .

## Run
    $ docker run --name microblog -d -p 8000:5000 \
    -e OPENSEARCH_URL=elasticsearch \
    -e CELERY_BROKER_URL=redis://redis:6379/0 \
    -e CELERY_RESULT_BACKEND=redis://redis:6379/0 \
    -e DATABASE_URL=mysql+pymysql://microblog:<database-password>@mysql/microblogdb \
    --network microblog-network microblog:latest