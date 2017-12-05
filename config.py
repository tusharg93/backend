    # -*- coding: utf-8 -*-
import datetime
import os

#from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

# ***********************************
# Settings all environments



#SECURITY_EMAIL_SENDER = 'no-reply@gmail.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = False
MAIL_USE_SSL = True


SESSION_TYPE = 'sqlalchemy'
SESSION_SQLALCHEMY_TABLE = 'login_sessions'
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s \n',
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
        },
        # 'sentry': {
        #     'format': '[%(asctime)s][%(levelname)s] %(name)s '
        #               '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
        #     'datefmt': '%Y-%m-%d %H:%M:%S %z',
        # }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        # 'sentry': {
        #     'level': 'INFO',
        #     'class': 'raven.handlers.logging.SentryHandler',
        #     # 'dsn': 'https://217ceffaab8c458d9fa97127b81b383d:7547c5b392674130be5082e78e9da806@sentry.io/121842',
        #     'formatter': 'sentry'
        # },
    },

    'loggers': {
        '': {
            'propagate': False,
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['APP_SECRET_KEY']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
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
    LOGGING = LOGGING

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
