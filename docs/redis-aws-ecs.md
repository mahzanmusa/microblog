# 🚀 Redis on AWS ECS Fargate (Development Guide)

This guide outlines how to deploy a **single-node Redis instance** on AWS ECS Fargate for development purposes. It covers infrastructure setup, application configuration, and testing strategies (including Hybrid Cloud testing).

---

## 🏗️ Architecture Overview

* **Compute:** AWS Fargate (Serverless, no EC2 management).
* **Networking:** Private VPC (Service-to-Service communication).
* **Discovery:** AWS Cloud Map (Internal DNS: `redis.dev.local`).
* **Access:** * **Internal:** Apps in ECS connect via `redis.dev.local`.
    * **External (Dev):** Local machines connect via **Public IP** (restricted by Security Group) or **SSM Tunnel**.

---

## ✅ Prerequisites

* AWS Account with active billing.
* **VPC** with at least one Public Subnet (for external access) or Private Subnet (for internal-only).
* **Python 3.x** installed locally.
* **AWS CLI** configured (`aws configure`).

---

## 🛠️ Step 1: Create Security Group

1.  Go to **EC2 Console** → **Security Groups** → **Create security group**.
2.  **Name:** `ecs-redis-dev-sg`
3.  **Inbound Rules:**
    | Type       | Port | Source         | Description |
    | :---       | :--- | :---           | :--- |
    | Custom TCP | 6379 | `My IP`        | Allows YOUR local laptop (for testing) |
    | Custom TCP | 6379 | `sg-xxxxxxxxx` | The Security Group ID of your ECS Web App |

---

## 📦 Step 2: Create ECS Task Definition

1.  Go to **ECS Console** → **Task Definitions** → **Create new Task Definition**.
2.  **Settings:**
    * **Launch Type:** Fargate
    * **CPU:** `.25 vCPU`
    * **Memory:** `.5 GB`
3.  **Container Details:**
    * **Image:** `public.ecr.aws/docker/library/redis:alpine`
    * **Port:** `6379`
    * **Command:** `redis-server,--requirepass,<your-password>`
4.  **Storage (Optional):** Add a Volume if you need data persistence across restarts.

---

## 🚀 Step 3: Create ECS Service

1.  Go to **Cluster** → **Services** → **Create**.
2.  **Compute Options:** Fargate.
3.  **Deployment:**
    * **Service Name:** `redis-service`
    * **Desired Tasks:** `1`
4.  **Networking:**
    * **VPC:** Select your development VPC.
    * **Subnets:** **Public Subnet** (required if you want to test from your laptop without a VPN/Bastion).
    * **Security Group:** Select `ecs-redis-dev-sg`.
    * **Public IP:** **ENABLED** (Critical for local testing).
5.  **Service Discovery:**
    * Check "Use Service Discovery".
    * **Namespace:** `dev.local`
    * **Service Name:** `redis`
    * *(Resulting Endpoint: `redis.dev.local`)*

---

## 💻 Step 4: Configure Your Application

Use Environment Variables to manage connections. This allows code to run locally (using Public IP) and in production (using Internal DNS) without changes.

**File:** `.env` (Do not commit to GitHub!)
```ini
# For Local Testing (Use the Task's Public IP)
REDIS_URL=AUTO or <your-redis-ip>
REDIS_PASSWORD=<your-password>
REDIS_PORT=6379

# For Production/ECS (Use the Service Discovery Name)
# REDIS_HOST=redis.dev.local
```

1.  Start the Worker (Terminal 1). Windows users must use --pool=solo
```
cd tests
python -m celery -A test_redis_worker_1 worker --loglevel=info --pool=solo
```

2.  Trigger a Task (Terminal 2)
```
cd tests
python test_redis_client_2.py
```