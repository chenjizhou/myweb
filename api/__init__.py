# -*- coding: utf-8 -*-
import os
from logging.config import dictConfig

import redis
import yaml
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config_map, logging_config_file_map

# database instant
db = SQLAlchemy()
# redis instant
redis_store = None
# get the .env config
env = os.getenv("ENVIRONMENT") if os.getenv("ENVIRONMENT") is not None else "develop"


# factory pattern
def create_app():
    app = Flask(__name__)
    config_class = config_map.get(env)
    app.config.from_object(config_class)

    logging_config_file = logging_config_file_map.get(env, None)
    if logging_config_file:
        with open(logging_config_file, "r") as logging_yaml:
            dictConfig(yaml.safe_load(logging_yaml.read()))

    # init db for app
    db.init_app(app)
    # init redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # use flask-session to store session in redis
    Session(app)
    # set flask CSRF protection
    CSRFProtect(app)

    # register bleu print
    from api.user.view import user_blueprint
    app.register_blueprint(user_blueprint)

    return app
