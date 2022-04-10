#Import statements
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os

# Application instances
app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
db          = SQLAlchemy(app)
migrate     = Migrate(app, db)
moment      = Moment(app)
login       = LoginManager(app)
login.login_view = 'login'

# Email configuration details
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth    =   None

        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'] , app.config['MAIL_PASSWORD'])
        secure = None

        if app.config['MAIL_USE_TLS']:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
            ,fromaddr='udiot@' + app.config['MAIL_SERVER']
            ,toaddrs=app.config['ADMINS']
            ,subject='Takaici App Failure'
            ,credentials=auth, secure=secure)

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
         os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/takaici.log', maxBytes=10240,backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Takaici startup...')

#Search functionality
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
from app import routes, models
