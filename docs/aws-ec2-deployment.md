EC2 OS - Amazon Linux 2023

'''
$ sudo yum -y update
$ sudo yum -y install python3.13
$ sudo yum -y install python3-devel
$ sudo yum -y install postfix nginx git
$ sudo yum install python3-pip -y
$ pip3 install supervisor

$ git clone https://github.com/mahzanmusa/microblog.git
$ cd microblog
$ python3.13 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ pip install gunicorn pymysql cryptography

'''