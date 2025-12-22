# microblog
Project based learning for Python: Microblog with Flask

Tutorial from [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

## Setting up the environment:

1.  Creating a directory where the project will live
```
    $ mkdir microblog
    $ cd microblog
```

2.  Creates a virtual environment named venv
```
    $ python3 -m venv venv
```

3.  Activate your brand new virtual environment (Windows Powershell)
```
    $ venv\Scripts\Activate.ps1
    (venv) $ _
```

## Installing the dependencies:

### Method 1: Running pip install based on requirement.txt file:
```
    (venv) $ pip install -r requirements.txt
```

Update requirements.txt file (if there's any changes)
```
    (venv) $ pip freeze > requirements.txt
```

### Method 2: Installing packages one by one:
1.  Install Flask
```
    (venv) $ pip install flask
```

2.  Register environment variables to be automatically used when run the
    flask command
```
    (venv) $ pip install python-dotenv
```

3.  Install Flask-WTF
```
    (venv) $ pip install flask-wtf
```

4.  Install Flask-SQLAlchemy
```
    (venv) $ pip install flask-sqlalchemy
```

5.  Install Flask-Migrate
```
    (venv) $ pip install flask-migrate
```

6.  Create the migration repository for microblog database model
```
    (venv) $ flask db init
```

7. To apply the changes to the database, or create tables
```
    (venv) $ flask db upgrade
```

8. Install Flask-Login
```
    (venv) $ pip install flask-login
```

9. Install Email() validator
```
    (venv) $ pip install email-validator
```

10. SMTP debugging server & start a debugging email server
```
    (venv) $ pip install aiosmtpd
    (venv) $ aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
```

11. Package for actual sending of emails
```
    (venv) $ pip install flask-mail
```

12. Password reset links have secure token. To generate these tokens, use JSON Web Tokens
```
    (venv) $ pip install pyjwt
```

13. Install Flask-Moment, for date and time rendering
```
    (venv) $ pip install flask-moment
```

14. Install Flask-Babel for Internationalization and Localization
```
    (venv) $ pip install flask-babel
```

15. Create translation .pot file, & create translation for <language-code>, & compile to format efficient used at run-time
```
    (venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .
    (venv) $ pybabel init -i messages.pot -d app/translations -l <language-code>
    (venv) $ pybabel compile -d app/translations

    #To update translation file:
    (venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .
    (venv) $ pybabel update -i messages.pot -d app/translations

    #Or use provided cli.py commands:
    (venv) $ flask translate init <language-code>
    (venv) $ flask translate update
    (venv) $ flask translate compile
```

16. Install language detection library
```
    (venv) $ pip install langdetect
```

17. Install HTTP Client for AJAX requests implementation
```
    (venv) $ pip install requests
```

18. Install boto3 library, official AWS SDK for Python. For AWS language translation service 
```
     (venv) $ pip install boto3
```

19. Install celery for message queue using Redis. Then running the Celery worker 
```
     (venv) $ pip install celery[redis]
     (venv) $ celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

## Add Flask environment file .flaskenv
    FLASK_APP=microblog.py
    FLASK_DEBUG=0

## Add environment file .env
    SECRET_KEY=a-really-long-and-unique-key-that-nobody-knows
    MAIL_SERVER=localhost
    MAIL_PORT=8025
    MS_TRANSLATOR_KEY=<your-azure-translator-key>
    MS_TRANSLATOR_REGION=<your-azure-region>
    AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
    AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
    AWS_DEFAULT_REGION=<your-aws-region>
    CELERY_BROKER_URL=<message-broker-url>
    CELERY_RESULT_BACKEND=<message-broker-backend>

## Unit Tests
    python -m unittest tests/test_general.py