from celery import Celery
import os
from dotenv import load_dotenv

# COMMAND TO RUN: python -m celery -A test_redis_worker_1 worker --loglevel=info --pool=solo

load_dotenv()

# The format is: redis://:password@host:port/db
# We use DB 0 for the broker (queue) and DB 1 for results to keep them clean
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

# --- Initialize Celery ---
app = Celery('test_app', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Optional: Tweak settings for testing
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Kuala_Lumpur',
    enable_utc=True,
)

# --- Define a Simple Task ---
@app.task
def add(x, y):
    return x + y