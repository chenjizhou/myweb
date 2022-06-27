# -*- coding: utf-8 -*-
import redis
import os
from os import path

basedir = os.path.abspath(path.join(os.path.dirname(__file__), "."))


class Config(object):
    # basic config
    DEBUG = True
    SECRET_KEY = "DQSF2ZE2ZE*EZA*7879"

    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    # database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@"+DB_HOST+":3306/mydb"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_PORT = 6379

    # flask-session
    REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # hide session_id in cookie
    PERMANENT_SESSION_LIFETIME = 86400  # session life time, seconds


# develop env
class DevelopmentConfig(Config):
    pass


# prod env
class ProductionConfig(Config):
    DEBUG = True


config_map = {
    "develop": DevelopmentConfig,
    "production": ProductionConfig
}

logging_config_file_map = dict(
        develop=os.path.join(basedir, "logging-develop.yml"),
        production=os.path.join(basedir, "logging-production.yml"),
)
