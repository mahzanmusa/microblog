import os
from dotenv import load_dotenv

# Try to import the utility; handle case where boto3 is not installed (e.g., minimal local env)
try:
    from app.aws_utils import get_fargate_public_ip
except ImportError as e:
    print(f"DEBUG: Import failed because: {e}")
    get_fargate_public_ip = None

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

    #CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    #CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

    #OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL') or 'localhost'
    OPENSEARCH_PORT = os.environ.get('OPENSEARCH_PORT') or '9200'
    OPENSEARCH_USERNAME = os.environ.get('OPENSEARCH_USERNAME')
    OPENSEARCH_PASSWORD = os.environ.get('OPENSEARCH_PASSWORD')
    OPENSEARCH_USE_SSL = os.environ.get('OPENSEARCH_USE_SSL') or 'False'
    OPENSEARCH_VERIFY_CERTS = os.environ.get('OPENSEARCH_VERIFY_CERTS') or 'False'
    OPENSEARCH_SERVICE = os.environ.get('OPENSEARCH_SERVICE')

    # --- AUTO-DISCOVERY LOGIC ---
    _os_url = os.environ.get('OPENSEARCH_URL')

    # Case A: Explicit URL in .env (e.g., 'localhost' for offline dev) -> Use it.
    if _os_url and _os_url != 'AUTO':
        OPENSEARCH_URL = _os_url
        print(f"Using configured OpenSearch Host: {OPENSEARCH_URL}")

    # Case B: 'AUTO' requested or missing, and we have the utility -> Try AWS Lookup.
    elif get_fargate_public_ip:
        print("Auto-discovering OpenSearch IP from AWS ECS...")
        found_ip = get_fargate_public_ip('dev-cluster', 'opensearch-service')
        
        if found_ip:
            # Construct the full host string
            OPENSEARCH_URL = found_ip
            print(f"Auto-discovery success. Target: {OPENSEARCH_URL}")
        else:
            # Fallback if AWS lookup fails (prevents crash, defaults to localhost)
            OPENSEARCH_URL = 'localhost'
            print("Auto-discovery failed. Falling back to 'localhost'.")
    
    # Case C: No utility available (boto3 missing) -> Fallback.
    else:
        OPENSEARCH_URL = 'localhost'

    # Construct full URL for clients that need it (optional, depends on your client lib)
    # Note: AWS OpenSearch usually requires HTTPS. Local Docker usually runs HTTP.
    #_protocol = 'https' if OPENSEARCH_HOST != 'localhost' else 'http'
    #OPENSEARCH_FULL_URL = f"{_protocol}://{OPENSEARCH_HOST}:{OPENSEARCH_PORT}"

    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'

    # --- AUTO-DISCOVERY LOGIC FOR REDIS ---
    _redis_url = os.environ.get('REDIS_URL')

    # Case A: Explicit URL in .env (e.g., 'localhost' for offline dev) -> Use it.
    if _redis_url and _redis_url != 'AUTO':
        REDIS_URL = _redis_url
        print(f"Using configured Redis Host: {REDIS_URL}")

    # Case B: 'AUTO' requested or missing, and we have the utility -> Try AWS Lookup.
    elif get_fargate_public_ip:
        print("Auto-discovering Redis IP from AWS ECS...")
        found_ip = get_fargate_public_ip('dev-cluster', 'redis-service')
        
        if found_ip:
            # Construct the full host string
            REDIS_URL = found_ip
            print(f"Auto-discovery success. Target: {REDIS_URL}")
        else:
            # Fallback if AWS lookup fails (prevents crash, defaults to localhost)
            REDIS_URL = 'localhost'
            print("Auto-discovery REDIS failed. Falling back to 'localhost'.")
    
    # Case C: No utility available (boto3 missing) -> Fallback.
    else:
        REDIS_URL = 'localhost'
        #print('get_fargate_public_ip:',get_fargate_public_ip)

    # Construct full URL for clients that need it (optional, depends on your client lib)
    # Note: AWS OpenSearch usually requires HTTPS. Local Docker usually runs HTTP.
    # redis://:YourStrongPassword123@13.217.58.192:6379/0
    # redis://13.217.58.192:6379/0
    if not REDIS_PASSWORD:
        CELERY_BROKER_URL = f"redis://{REDIS_URL}:{REDIS_PORT}/0"
        CELERY_RESULT_BACKEND = f"redis://{REDIS_URL}:{REDIS_PORT}/1"
    else:
        CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_URL}:{REDIS_PORT}/0"
        CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_URL}:{REDIS_PORT}/1"



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