# Redis Deployment - For Message Queue

## Create the Network (if not already)
    $ docker network create microblog-network

## Install OpenSearch Docker locally
    $ docker run --name redis -d -p 6379:6379 --network microblog-network redis:latest

## .env file on your local
You can leave it empty, as it will take default values ```redis://localhost:6379/0```

