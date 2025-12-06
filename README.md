# microblog
Project based learning for Python: Microblog with Flask

Tutorial from [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

Setting up the environment:

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

4.  Install Flask
```
    (venv) $ pip install flask
```

5.  Register environment variables to be automatically used when run the
    flask command
```
    (venv) $ pip install python-dotenv
```

6.  Install Flask-WTF
```
    (venv) $ pip install flask-wtf
```

7.  Install Flask-SQLAlchemy
```
    (venv) $ pip install flask-sqlalchemy
```

8.  Install Flask-Migrate
```
    (venv) $ pip install flask-migrate
```

9.  Create the migration repository for microblog database model
```
    (venv) $ flask db init
```

10. To apply the changes to the database, or create tables
```
    (venv) $ flask db upgrade
```

11. Install Flask-Login
```
    (venv) $ pip install flask-login
```

12. Install Email() validator
```
    (venv) $ pip install email-validator
```

13. SMTP debugging server & start a debugging email server
```
    (venv) $ pip install aiosmtpd
    (venv) $ aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
```

14. Package for actual sending of emails ***
```
    (venv) $ pip install flask-mail
```

15. Password reset links have secure token. To generate these tokens, use JSON Web Tokens
```
    (venv) $ pip install pyjwt
```

16. Install Flask-Moment, for date and time rendering
```
    (venv) $ pip install flask-moment
```

17. Install Flask-Babel for Internationalization and Localization
```
    (venv) $ pip install flask-babel
```

18. Create translation .pot file, & create translation for <language-code>, & compile to format efficient used at run-time
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

Add Flask environment file .flaskenv
```
FLASK_APP=microblog.py
FLASK_DEBUG=0
MAIL_SERVER=localhost
MAIL_PORT=8025
```