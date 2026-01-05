import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
 
    admins_env = os.getenv('ADMINS')
    if admins_env:
        # splits "a,b" into ['a', 'b'] and removes surrounding whitespace just in case
        ADMINS = [email.strip() for email in admins_env.split(',')]
    else:
        # Fallback to empty list if not set
        ADMINS = []

    POSTS_PER_PAGE = 25

    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    MS_TRANSLATOR_REGION = os.environ.get('MS_TRANSLATOR_REGION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

    OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL') or 'localhost'
    OPENSEARCH_PORT = os.environ.get('OPENSEARCH_PORT') or '9200'
    OPENSEARCH_USERNAME = os.environ.get('OPENSEARCH_USERNAME')
    OPENSEARCH_PASSWORD = os.environ.get('OPENSEARCH_PASSWORD')
    OPENSEARCH_USE_SSL = os.environ.get('OPENSEARCH_USE_SSL') or 'False'
    OPENSEARCH_VERIFY_CERTS = os.environ.get('OPENSEARCH_VERIFY_CERTS') or 'False'
    OPENSEARCH_SERVICE = os.environ.get('OPENSEARCH_SERVICE')


class ProductionConfig(Config):
    # In production, we override the property to enforce strict checking
    @property
    def SECRET_KEY(self):
        # 1. Attempt to get the key
        key = os.environ.get('SECRET_KEY')
        
        # 2. Check explicitly if it exists
        if not key:
            # 3. CRITICAL: Stop the app immediately if missing
            raise ValueError("CRITICAL: SECRET_KEY environment variable is not set. Application cannot start.")
        
        return key