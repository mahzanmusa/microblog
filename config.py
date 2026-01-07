import os
from dotenv import load_dotenv
from aws_discovery import resolve_service_host

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Mail Settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
 
    admins_env = os.getenv('ADMINS')
    ADMINS = [email.strip() for email in admins_env.split(',')] if admins_env else []

    POSTS_PER_PAGE = 25
    LANGUAGES = ['en', 'es']
    
    # Translator & AWS Keys
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    MS_TRANSLATOR_REGION = os.environ.get('MS_TRANSLATOR_REGION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')

    # OpenSearch Params
    OPENSEARCH_PORT = os.environ.get('OPENSEARCH_PORT') or '9200'
    OPENSEARCH_USERNAME = os.environ.get('OPENSEARCH_USERNAME')
    OPENSEARCH_PASSWORD = os.environ.get('OPENSEARCH_PASSWORD')
    OPENSEARCH_USE_SSL = os.environ.get('OPENSEARCH_USE_SSL') or 'False'
    OPENSEARCH_VERIFY_CERTS = os.environ.get('OPENSEARCH_VERIFY_CERTS') or 'False'
    OPENSEARCH_SERVICE = os.environ.get('OPENSEARCH_SERVICE')

    # AWS ECS Configuration
    ECS_CLUSTER = os.environ.get('ECS_CLUSTER') or 'dev-cluster'
    ECS_OPENSEARCH_SERVICE_NAME = os.environ.get('ECS_OPENSEARCH_SERVICE_NAME') or 'opensearch-service'
    ECS_REDIS_SERVICE_NAME = os.environ.get('ECS_REDIS_SERVICE_NAME') or 'redis-service'

    # --- AUTO-DISCOVERY LOGIC (OpenSearch) ---
    OPENSEARCH_URL = resolve_service_host('OPENSEARCH_URL', ECS_CLUSTER, ECS_OPENSEARCH_SERVICE_NAME)

    # Redis Params
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'

    # --- AUTO-DISCOVERY LOGIC (Redis) ---
    REDIS_URL = resolve_service_host('REDIS_URL', ECS_CLUSTER, ECS_REDIS_SERVICE_NAME)
    
    # Final Celery URLs
    if not REDIS_PASSWORD:
        CELERY_BROKER_URL = f"redis://{REDIS_URL}:{REDIS_PORT}/0"
        CELERY_RESULT_BACKEND = f"redis://{REDIS_URL}:{REDIS_PORT}/1"
    else:
        CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_URL}:{REDIS_PORT}/0"
        CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_URL}:{REDIS_PORT}/1"

class ProductionConfig(Config):
    @property
    def SECRET_KEY(self):
        key = os.environ.get('SECRET_KEY')
        if not key:
            raise ValueError("CRITICAL: SECRET_KEY environment variable is not set.")
        return key