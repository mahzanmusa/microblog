# AWS OpenSearch Serverless Connection Guide

This document outlines the specific configurations required to successfully connect a local Python application (or EC2 instance) to AWS OpenSearch Serverless.

## 1. IAM Permissions (The "Key")
Before configuring OpenSearch, the IAM Identity (User or Role) accessing the service must have permission to talk to the API.

* **Requirement:** The IAM User or Role must have an attached policy allowing Serverless operations.
* **Recommended Policy:** `AmazonOpenSearchServiceFullAccess`
* **Minimal Inline Policy:**
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "aoss:*",
                "Resource": "*"
            }
        ]
    }
    ```

## 2. Network Access Policy (The "Gate")
Controls connectivity to the endpoint.

* **Location:** OpenSearch Service > Serverless > Network policies
* **Access Type:** `Public` (Required for access from local laptop or non-VPC sources).
* **Resource Type:** Enable for both:
    * `Collection endpoint` (API access)
    * `OpenSearch Dashboards endpoint` (UI access)

## 3. Data Access Policy (The "Lock")
Controls who can read/write data inside the collection. This is distinct from IAM permissions.

* **Location:** OpenSearch Service > Serverless > Data access policies
* **Principal:** Must explicitly list the ARN of the caller.
    * Local Dev: `arn:aws:iam::1234567890:user/your-local-user`
    * EC2 Prod: `arn:aws:iam::1234567890:role/your-ec2-role`
* **Rules:** Must match the Collection and Index names exactly.
    * **Resource (Collection):** `collection/microblog` (or `collection/*`)
    * **Resource (Index):** `index/microblog/*` (or `index/*/*`)
* **Permissions:** Grant all (Create, Delete, Update, Describe for both Collection and Index).

## 4. Client-Side Configuration (Critical)
OpenSearch Serverless (`aoss`) behaves differently than standard OpenSearch (`es`).

| Setting | Value | Reason |
| :--- | :--- | :--- |
| **Service Name** | `aoss` | **Crucial.** Standard `es` signing will result in `403 Forbidden`. |
| **Port** | `443` | Serverless does not use port 9200. |
| **Protocol** | `https` | Plain http is not supported. |
| **Timeout** | `60` | Cold starts can take >10s. Default timeouts will fail. |
| **Refresh** | `False` | **Crucial.** Do not use `refresh=True` in index operations. It causes `400 Bad Request`. |

---

## 5. How to Test the Connection

### Method A: Quick Network Check (Curl)
Run this from your terminal to verify the Network Policy is open.
* **Expected:** `404 Not Found` (This is good! It means you reached the server).
* **Failure:** Hangs/Timeout (Network blocked).

```bash
curl -v https://<your-collection-id>.us-east-1.aoss.amazonaws.com
```


### Method B: Python Diagnostic Script
Run this script to verify Identity, Policy matching, and Connectivity.

```python
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

# CONFIGURATION
host = '<your-collection-id>.us-east-1.aoss.amazonaws.com'
region = 'us-east-1'
service = 'aoss' # MUST be aoss

# 1. Get Credentials
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

# 2. Print Identity (Verify this ARN is in your Data Access Policy)
print(f"Identity: {boto3.client('sts').get_caller_identity()['Arn']}")

# 3. Connect
client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=60
)

# 4. Test
try:
    print(client.info())
    print("\nSUCCESS: Connected to OpenSearch Serverless!")
except Exception as e:
    print(f"\nERROR: {e}")
```

## 6. Config .env File on your environment

### .env file
    OPENSEARCH_URL=<your-opensearch-url>
    OPENSEARCH_PORT=443
    OPENSEARCH_USE_SSL=True
    OPENSEARCH_VERIFY_CERTS=True
    OPENSEARCH_SERVICE=aoss

### Reindex the Post table
    $ source venv/bin/activate
    (venv) $ flask shell
    >>> from app.models import Post
    >>> Post.reindex()
    >>> exit()
