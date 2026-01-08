# Redis Deployment - For Message Queue

## Create the Network (if not already)
    $ docker network create microblog-network

## Install OpenSearch Docker locally
    $ docker run --name redis -d -p 6379:6379 --network microblog-network redis:latest

## .env file on your local
You can leave it empty, as it will take default values ```redis://localhost:6379/0```

## To test locally:
1.  Start the Worker (Terminal 1). Windows users must use --pool=solo
```
cd tests
python -m celery -A test_redis_worker_1 worker --loglevel=info --pool=solo
```

2.  Trigger a Task (Terminal 2)
```
cd tests
python test_redis_client_2.py
```