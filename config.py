import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# --- HELPER FUNCTION MOVED HERE TO PREVENT CIRCULAR IMPORT ---
def get_fargate_public_ip(cluster_name, service_name, region='us-east-1'):
    """
    Finds the current Public IP of an ECS Fargate Service via ENI lookup.
    """
    try:
        session = boto3.Session()
        if not session.get_credentials():
            print("No AWS credentials found. Skipping Fargate IP lookup.")
            return None

        ecs = session.client('ecs', region_name=region)
        ec2 = session.client('ec2', region_name=region)

        # 1. List running tasks
        tasks = ecs.list_tasks(cluster=cluster_name, serviceName=service_name)
        if not tasks.get('taskArns'): 
            return None

        # 2. Describe task to find Network Interface (ENI)
        task_desc = ecs.describe_tasks(cluster=cluster_name, tasks=tasks['taskArns'])
        if not task_desc['tasks']:
            return None
            
        current_task = task_desc['tasks'][0]
        
        if current_task['lastStatus'] != 'RUNNING': 
            return None

        eni_id = next(
            (detail['value'] 
             for attachment in current_task['attachments'] 
             if attachment['type'] == 'ElasticNetworkInterface' 
             for detail in attachment['details'] 
             if detail['name'] == 'networkInterfaceId'), 
            None
        )
        
        if not eni_id: 
            return None

        # 3. Get IP from EC2
        eni_desc = ec2.describe_network_interfaces(NetworkInterfaceIds=[eni_id])
        return eni_desc['NetworkInterfaces'][0]['Association']['PublicIp']

    except (NoCredentialsError, ClientError, Exception) as e:
        print(f"AWS Auto-discovery skipped: {e}")
        return None
# -------------------------------------------------------------

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

    # --- AUTO-DISCOVERY LOGIC (OpenSearch) ---
    _os_url = os.environ.get('OPENSEARCH_URL')

    if _os_url and _os_url != 'AUTO':
        OPENSEARCH_URL = _os_url
        print(f"Using configured OpenSearch Host: {OPENSEARCH_URL}")
    else:
        print("Auto-discovering OpenSearch IP from AWS ECS...")
        # Update 'dev-cluster' and 'opensearch-service' to your ACTUAL AWS names if different
        found_ip = get_fargate_public_ip('dev-cluster', 'opensearch-service')
        
        if found_ip:
            OPENSEARCH_URL = found_ip
            print(f"Auto-discovery success. Target: {OPENSEARCH_URL}")
        else:
            OPENSEARCH_URL = 'localhost'
            print("Auto-discovery failed. Falling back to 'localhost'.")

    # Redis Params
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'

    # --- AUTO-DISCOVERY LOGIC (Redis) ---
    _redis_url = os.environ.get('REDIS_URL')

    if _redis_url and _redis_url != 'AUTO':
        REDIS_URL = _redis_url
        print(f"Using configured Redis Host: {REDIS_URL}")
    else:
        print("Auto-discovering Redis IP from AWS ECS...")
        # Update 'dev-cluster' and 'redis-service' to your ACTUAL AWS names if different
        found_ip = get_fargate_public_ip('dev-cluster', 'redis-service')
        
        if found_ip:
            REDIS_URL = found_ip
            print(f"Auto-discovery success. Target: {REDIS_URL}")
        else:
            REDIS_URL = 'localhost'
            print("Auto-discovery REDIS failed. Falling back to 'localhost'.")
    
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