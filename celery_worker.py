import os

# --- CRITICAL FIX: Kill the zombie variable before anything else loads ---
if 'CELERY_RESULT_BACKEND' in os.environ:
    del os.environ['CELERY_RESULT_BACKEND']
# -----------------------------------------------------------------------

from app import create_app
from app.celery_utils import make_celery

app = create_app()
celery = make_celery(app)