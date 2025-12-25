import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from app.celery_utils import make_celery
from opensearchpy import OpenSearch, RequestsHttpConnection

def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
moment = Moment()
babel = Babel()


def str_to_bool(s):
    if isinstance(s, bool):
        return s
    return str(s).lower() in ('true', '1', 't')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    # Initialize Celery and attach it to the app
    celery = make_celery(app)
    app.extensions['celery'] = celery
    app.celery = celery

    if app.config['OPENSEARCH_URL']:
        # 1. Default auth to None (Safe for local dev without auth)
        auth = None 
        
        # 2. Check if we are running in "AWS Mode"
        # We check if OPENSEARCH_SERVICE is set (e.g., 'aoss' or 'es')
        if app.config.get('OPENSEARCH_SERVICE'):
            try:
                # Only import boto3 if we actually need it
                import boto3
                from opensearchpy import AWSV4SignerAuth
                
                credentials = boto3.Session().get_credentials()
                region = boto3.Session().region_name
                service = app.config['OPENSEARCH_SERVICE']
                
                # Overwrite 'auth' with the AWS Signer
                auth = AWSV4SignerAuth(credentials, region, service)
            except Exception as e:
                app.logger.warning(f"Failed to setup AWS Auth: {e}")
                # auth remains None here, or you could raise an error

        # 3. Initialize the Client
        app.opensearchpy = OpenSearch(
            hosts=[{'host': app.config['OPENSEARCH_URL'], 'port': app.config['OPENSEARCH_PORT']}],
            http_auth=auth, # <--- Works if this is None OR AWSV4SignerAuth
            use_ssl=str_to_bool(app.config['OPENSEARCH_USE_SSL']),     
            verify_certs=str_to_bool(app.config['OPENSEARCH_VERIFY_CERTS']),
            connection_class=RequestsHttpConnection,
            timeout=60
        )
   
  #  app.opensearchpy = OpenSearch(
   #     hosts=[{'host': app.config['OPENSEARCH_URL'], 'port': app.config['OPENSEARCH_PORT']}],
   #     http_compress=True,
   #     use_ssl=str_to_bool(app.config['OPENSEARCH_USE_SSL']),     
   #     verify_certs=str_to_bool(app.config['OPENSEARCH_VERIFY_CERTS']),
   #     http_auth=app.config['OPENSEARCH_HTTP_AUTH']      
   #     ) \
   #     if app.config['OPENSEARCH_URL'] else None

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from app import models
