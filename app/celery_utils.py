from celery import Celery

def make_celery(app):
    # Initialize Celery WITHOUT passing broker/backend here.
    # We will let config_from_object handle it.
    celery = Celery(app.import_name)
    
    # Load configuration from Flask.
    # namespace='CELERY' tells Celery to read 'CELERY_BROKER_URL' 
    # and map it to 'broker_url' automatically.
    celery.config_from_object(app.config, namespace='CELERY')

    # Create a context-aware task base class
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery