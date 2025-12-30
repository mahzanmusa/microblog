# MySQL Deployment - Docker Container

## Create the Network (if not already)
    $ docker network create microblog-network

## Build & Run
    $ docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=microblogdb -e MYSQL_USER=microblog \
    -e MYSQL_PASSWORD=<database-password> \
    --network microblog-network \
    mysql:latest
