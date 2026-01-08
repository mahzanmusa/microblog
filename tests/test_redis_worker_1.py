import sys
import os
from celery import Celery

# --- 1. SETUP PATHS (So we can find config.py) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

from config import Config 

# COMMAND TO RUN: python -m celery -A test_redis_worker_1 worker --loglevel=info --pool=solo

# The format is: redis://:password@host:port/db
# We use DB 0 for the broker (queue) and DB 1 for results to keep them clean
CELERY_BROKER_URL = Config.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = Config.CELERY_RESULT_BACKEND

#print(CELERY_BROKER_URL, CELERY_RESULT_BACKEND)

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