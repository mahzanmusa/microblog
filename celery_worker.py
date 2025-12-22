from app import create_app
from app.celery_utils import make_celery

app = create_app()
celery = make_celery(app)

# This forces the worker to load the tasks module and register the functions
from app import tasks