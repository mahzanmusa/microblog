# Redis Deployment - For Message Queue

## Create the Network
    $ docker network create microblog-network

## Install OpenSearch Docker locally
    $ docker run --name redis -d -p 6379:6379 --network microblog-network redis:latest

## .env file on your local
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0

