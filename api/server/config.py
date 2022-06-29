# -*- coding: utf-8 -*-
import redis
import os
from os import path
from datetime import timedelta

basedir = os.path.abspath(path.join(os.path.dirname(__file__), "../.."))


class Config(object):
    # basic config
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@" + DB_HOST + ":3306/mydb"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_PORT = 6379

    # flask-session
    REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # hide session_id in cookie
    PERMANENT_SESSION_LIFETIME = 86400  # session life time, seconds


# testing env
class TestingConfig(Config):
    CONFIG_NAME = "testing"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@" + Config.DB_HOST + ":3306/mydb_testing"
    WTF_CSRF_ENABLED = False


# develop env
class DevelopmentConfig(Config):
    CONFIG_NAME = "development"
    DEBUG = True
    pass


# prod env
class ProductionConfig(Config):
    CONFIG_NAME = "production"
    DEBUG = False
    # todo define the production DB config here


config_map = {
    "testing": TestingConfig,
    "develop": DevelopmentConfig,
    "production": ProductionConfig
}

logging_config_file_map = dict(
        develop=os.path.join(basedir, "api", "server", "logging-develop.yml"),
        production=os.path.join(basedir, "api", "server", "logging-production.yml"),
)
