# EC2 OS - Amazon Linux 2023

## Install Python, dependencies, source code
    $ sudo yum -y install python3.13 python3-devel postfix nginx git python3-pip

    $ git clone https://github.com/mahzanmusa/microblog.git

    $ cd microblog

## Create .env file
    FLASK_ENV=production
    SECRET_KEY=<your-secret-key-for-forms>
    MAIL_SERVER=<your-smtp-server>
    MAIL_PORT=8025
    DATABASE_URL=mysql+pymysql://<db-username>:<db-password>@<db-url>:3306/<db-name>
    MS_TRANSLATOR_KEY=<ms-azure-translator-key>
    MS_TRANSLATOR_REGION=<ms-azure-region>
    AWS_ACCESS_KEY_ID=<aws-access-key-id>
    AWS_SECRET_ACCESS_KEY=<aws-secret-access-key>
    AWS_DEFAULT_REGION=<aws-region>
    CELERY_BROKER_URL=<message-broker-url>
    CELERY_RESULT_BACKEND=<message-broker-backend>
    OPENSEARCH_URL=<your-opensearch-url>
    OPENSEARCH_PORT=443
    OPENSEARCH_USE_SSL=True
    OPENSEARCH_VERIFY_CERTS=True
    OPENSEARCH_SERVICE=aoss

## Run in virtual environment, install components
    $ python3.13 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt
    (venv) $ pip install gunicorn pymysql cryptography

## Create database
    (venv) $ flask db upgrade

## Create SSL Certificate in AWS EC2
    $ sudo mkdir /etc/nginx/ssl

    $ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/selfsigned.key \
    -out /etc/nginx/ssl/selfsigned.crt

    # Common Name (CN): Paste your AWS address here

## Update nginx config file
    $ sudo nano /etc/nginx/nginx.conf

    server {
        listen 80;
        listen [::]:80;
        server_name _;  # Or your specific AWS address

        # THIS IS THE REDIRECT LINE
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name _;  # Or your AWS address

        # The SSL Keys you just made
        ssl_certificate /etc/nginx/ssl/selfsigned.crt;
        ssl_certificate_key /etc/nginx/ssl/selfsigned.key;

        # Proxy settings (Same as your HTTP block)
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            # Crucial: Tell Flask it's running over HTTPS
            proxy_set_header X-Forwarded-Proto https;
        }
    }

## Test and reload nginx
    $ sudo nginx -t
    $ sudo systemctl restart nginx

## Check nginx status:
    $ sudo systemctl status nginx

## Set systemd service file so apps runs automatically in the background
    $ sudo nano /etc/systemd/system/microblog.service

    [Unit]
    Description=Gunicorn instance to serve my Flask app
    After=network.target

    [Service]
    # The user you log in as (usually 'ec2-user' on Amazon Linux, or 'ubuntu')
    User=ec2-user               
    Group=nginx

    # The output from the 'pwd' command you ran earlier
    WorkingDirectory=/home/ec2-user/microblog

    # The specific path to the gunicorn executable you found with 'which gunicorn'
    # IMPORTANT: Ensure the bind address (127.0.0.1:8000) matches your Nginx config!
    ExecStart=/home/ec2-user/microblog/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 microblog:app

    Restart=always

    [Install]
    WantedBy=multi-user.target

## Reload
    $ sudo systemctl daemon-reload
    $ sudo systemctl start microblog
    $ sudo systemctl enable microblog

## Verify it's running
    $ sudo systemctl status microblog
