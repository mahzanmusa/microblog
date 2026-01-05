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
from config import Config, ProductionConfig
from app.celery_utils import make_celery
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

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

def init_opensearch(app):
    """
    Initializes OpenSearch client based on the environment:
    1. AWS Serverless: Uses AWSV4SignerAuth
    2. AWS ECS / Local: Uses Basic Auth (User/Pass)
    3. No Auth: Defaults to None
    """
    if not app.config.get('OPENSEARCH_URL'):
        return

    auth = None
    use_ssl = str_to_bool(app.config.get('OPENSEARCH_USE_SSL', True))
    verify_certs = str_to_bool(app.config.get('OPENSEARCH_VERIFY_CERTS', True))

    # STRATEGY 1: AWS Serverless (SigV4)
    # Triggered if 'OPENSEARCH_SERVICE' is set (e.g., 'aoss' or 'es')
    if app.config.get('OPENSEARCH_SERVICE'):
        try:
            import boto3
            credentials = boto3.Session().get_credentials()
            region = boto3.Session().region_name
            auth = AWSV4SignerAuth(credentials, region, app.config['OPENSEARCH_SERVICE'])
        except Exception as e:
            app.logger.warning(f"Failed to setup AWS Auth: {e}")

    # STRATEGY 2: Basic Auth (ECS or Local)
    # Triggered if Username/Password are provided in config
    elif app.config.get('OPENSEARCH_USERNAME') and app.config.get('OPENSEARCH_PASSWORD'):
        auth = (app.config['OPENSEARCH_USERNAME'], app.config['OPENSEARCH_PASSWORD'])

    # Initialize the Client
    app.opensearchpy = OpenSearch(
        hosts=[{
            'host': app.config['OPENSEARCH_URL'],
            'port': int(app.config.get('OPENSEARCH_PORT', 443))
        }],
        http_auth=auth,
        use_ssl=use_ssl,
        verify_certs=verify_certs,
        connection_class=RequestsHttpConnection,
        timeout=60
    )

import urllib3
# Suppress only the single warning from urllib3 needed.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_app(config_class=None):
    app = Flask(__name__)

    if not config_class:
        # Determine config based on FLASK_ENV or similar variable
        if os.environ.get('FLASK_ENV') == 'production':
            config_class = ProductionConfig
        else:
            config_class = Config

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

    # Initialize OpenSearch
    init_opensearch(app)
    
    # Initialize Celery and attach it to the app
    celery = make_celery(app)
    app.extensions['celery'] = celery
    app.celery = celery

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
                fromaddr=app.config['MAIL_USERNAME'],
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
