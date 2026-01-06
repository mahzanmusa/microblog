# OpenSearch on AWS ECS Fargate (Development Environment)

This repository documents the setup of a single-node OpenSearch instance running on **AWS ECS Fargate Spot** with persistent **EFS storage**. 

This configuration is optimized for a low-cost development environment (approx. **$5.75/month** if scheduled to run 4 hours/day).

## 📋 Architecture Overview

* **Compute:** AWS Fargate (Spot Capacity Provider) for cost efficiency (~70% savings vs On-Demand).
* **Storage:** AWS EFS (Elastic File System) for data persistence across container restarts.
* **Networking:** Public Subnet with Auto-assigned Public IP.
* **Security:** * Security Group acting as a firewall.
    * Basic Authentication enabled on OpenSearch.
    * IAM Roles for secure EFS access.

---

## 🛠️ Implementation Guide

### Step 1: Network & Security Groups
Create a Security Group (`opensearch-dev-sg`) to act as the firewall.

| Rule Type | Protocol | Port | Source | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Inbound** | TCP | `9200` | `My IP` | Allows you to connect to the API. |
| **Inbound** | NFS | `2049` | `opensearch-dev-sg` | **Crucial:** Allows the container to talk to itself (mount EFS). |

### Step 2: Persistent Storage (EFS)
Since Fargate containers are ephemeral, we use EFS to store indices.

1.  **Create File System:** Standard EFS, attached to the ECS VPC/Subnets.
2.  **Create Access Point:** This handles permission mapping for the OpenSearch user.
    * **Root Path:** `/data`
    * **POSIX User:** UID `1000` / GID `1000`
    * **Creation Permissions:** Owner UID `1000`, Owner GID `1000`, Permissions `755`.

### Step 3: IAM Permissions (Task Role)
Create an IAM Role (`ecs-opensearch-task-role`) for the **ECS Task**.
* **Trusted Entity:** Elastic Container Service Task.
* **Policy:** `AmazonElasticFileSystemClientReadWriteAccess`.

### Step 4: ECS Task Definition
Create a Fargate Task Definition with the following configuration:

* **Resources:** 2 vCPU, 4 GB RAM.
* **Task Role:** `ecs-opensearch-task-role` (Created in Step 3).
* **Environment Variables:**
    * `discovery.type` = `single-node`
    * `bootstrap.memory_lock` = `false`
    * `OPENSEARCH_JAVA_OPTS` = `-Xms1g -Xmx1g`
    * `network.host` = `0.0.0.0`
    * `OPENSEARCH_INITIAL_ADMIN_PASSWORD` = `YourStrongPassword1!`
* **Storage Configuration:**
    * **Volume:** Select EFS. Enable **"IAM Authentication"** and paste the **Access Point ID**.
    * **Mount Point:** Container path `/usr/share/opensearch/data`.

### Step 5: Launch Service
* **Capacity Provider:** `FARGATE_SPOT`.
* **Networking:** Public Subnet, **Auto-assign Public IP: ENABLED**.

---

## 🧪 Testing & Validation

Since the Public IP changes on every restart, retrieve the new IP from the ECS Console -> Task Details.

### 1. Check Connectivity
Use `curl` with the `-k` flag (to ignore self-signed certs) and `-u` for authentication.

```bash
curl -k -u admin:YourStrongPassword1! https://<PUBLIC_IP>:9200
```

### 2. Setup local environment
Permissions: Your laptop must be logged into AWS (via ```aws configure```) with a user that has permission to "read" ECS and EC2 data.
* Required Policy: ```AmazonECS_FullAccess``` (or ReadOnly) and ```AmazonEC2ReadOnlyAccess```.

---

## 🛠️ .env File on your environment

### .env file
    OPENSEARCH_URL=<your-opensearch-url>
    OPENSEARCH_PORT=9200
    OPENSEARCH_USERNAME=<your-opensearch-username>
    OPENSEARCH_PASSWORD=<your-opensearch-password>
    OPENSEARCH_USE_SSL=True
    # Important for self-signed certs
    OPENSEARCH_VERIFY_CERTS=False
    # Leave below empty to avoid triggering AWS SigV4
    OPENSEARCH_SERVICE=

### Reindex the Post table
    $ source venv/bin/activate
    (venv) $ flask shell
    >>> from app.models import Post
    >>> Post.reindex()
    >>> exit()