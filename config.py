import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    TESTING = os.environ.get('TESTING')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    # Database
    SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://root:usbw@localhost:3307/epl_predictor' # user is root, and password is usbw
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DOCUMENTS_PER_PAGE=10

# Configure Email. error report to the Admin emails
    MAIL_SERVER     =   os.environ.get('MAIL_SERVER')
    MAIL_PORT       =   int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS    =   os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME   =   os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD   =   os.environ.get('MAIL_PASSWORD')
    ADMINS          =   ['forkuorobinson@gmail.com','anotheremail@gmail.com']
