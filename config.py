# -*- coding: utf-8 -*-
import datetime
import os

#from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

# ***********************************
# Settings all environments



SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'poiuytresdfghjkloiuytrescvbnml;p98765rdcvbnmloiuytr'
#SECURITY_EMAIL_SENDER = 'no-reply@gmail.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'tushar202793@gmail.com'
MAIL_PASSWORD = 'qwert@123'

SESSION_TYPE = 'sqlalchemy'
SESSION_SQLALCHEMY_TABLE = 'login_sessions'
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['APP_SECRET_KEY']
    APP_KEY = "BYTa4u9d-dsc8GM1LtnQEjs9RZVgZzRGyPQ2bMQw"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://tushar:tushar1234@localhost/base_db"
    SQLALCHEMY_BINDS = {
        'base_db': "postgresql+psycopg2://tushar:tushar1234@localhost/base_db",
    }
    DATABASE_USER ="tushar"
    DATABASE_PASSWORD = "tushar1234"
    PERMANENT_SESSION_LIFETIME = PERMANENT_SESSION_LIFETIME
    SESSION_TYPE = SESSION_TYPE
    SESSION_SQLALCHEMY_TABLE = SESSION_SQLALCHEMY_TABLE


class ProductionConfig(Config):
    DEBUG = False
    LOCATION_LENGTH_MAX = 5


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    TESTING = True
    if os.environ.get('TEST_DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']
