# microblog
Project based learning for Python: Microblog with Flask

Tutorial from [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

Setting up the environment:

1.  Creating a directory where the project will live

```{=html}
<!-- -->
```
    $ mkdir microblog
    $ cd microblog

2.  Creates a virtual environment named venv

```{=html}
<!-- -->
```
    $ python3 -m venv venv

3.  Activate your brand new virtual environment (Windows Powershell)

```{=html}
<!-- -->
```
    $ venv\Scripts\Activate.ps1
    (venv) $ _

4.  Install Flask

```{=html}
<!-- -->
```
    (venv) $ pip install flask

5.  Register environment variables to be automatically used when run the
    flask command

```{=html}
<!-- -->
```
    (venv) $ pip install python-dotenv

6.  Install Flask-WTF

```{=html}
<!-- -->
```
    (venv) $ pip install flask-wtf

7.  Install Flask-SQLAlchemy

```{=html}
<!-- -->
```
    (venv) $ pip install flask-sqlalchemy

8.  Install Flask-Migrate

```{=html}
<!-- -->
```
    (venv) $ pip install flask-migrate

9.  Create the migration repository for microblog database model

```{=html}
<!-- -->
```
    (venv) $ flask db init

10. To apply the changes to the database, or create tables

```{=html}
<!-- -->
```
    (venv) $ flask db upgrade

11. Install Flask-Login

```{=html}
<!-- -->
```
    (venv) $ pip install flask-login

12. Install Email() validator

```{=html}
<!-- -->
```
    (venv) $ pip install email-validator
