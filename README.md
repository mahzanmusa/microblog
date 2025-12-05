# microblog
Project based learning for Python: Microblog with Flask

Tutorial from [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

Setting up the environment:

1. Creating a directory where the project will live
$ mkdir microblog
$ cd microblog

2. Creates a virtual environment named venv
$ python3 -m venv venv

3. Activate your brand new virtual environment (Windows Powershell)
$ venv\Scripts\Activate.ps1
(venv) $ _

4. Install Flask
(venv) $ pip install flask

5. Register environment variables to be automatically used when run the flask command
(venv) $ pip install python-dotenv

6. Install Flask-WTF
(venv) $ pip install flask-wtf

7. Install Flask-SQLAlchemy
(venv) $ pip install flask-sqlalchemy

8. Install Flask-Migrate
(venv) $ pip install flask-migrate

9. Create the migration repository for microblog database model
(venv) $ flask db init

10. To apply the changes to the database, or create tables
(venv) $ flask db upgrade

11. Install Flask-Login
(venv) $ pip install flask-login

12. Install Email() validator
(venv) $ pip install email-validator
