import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def get_fargate_public_ip(cluster_name, service_name, region='us-east-1'):
    """
    Finds the current Public IP of an ECS Fargate Service via ENI lookup.
    Returns None if running locally, offline, or if lookup fails.
    """
    try:
        # Check for credentials before attempting connection to avoid timeouts
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

    except (NoCredentialsError, ClientError) as e:
        # This catches expected AWS errors (offline, permissions)
        print(f"AWS Auto-discovery skipped: {e}")
        return None
    except Exception as e:
        # This catches unexpected logic errors
        print(f"Auto-discovery unexpected error: {e}")
        return None