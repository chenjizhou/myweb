# -*- coding: utf-8 -*-
import os
from logging.config import dictConfig

import redis
import yaml
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from api.server.config import config_map, logging_config_file_map, basedir


#######################
#### Configuration ####
#######################
# instantiate global scope, do not set any arguments
# Bootstrap instant
bootstrap = Bootstrap()
# database instant
db = SQLAlchemy()
# redis instant
redis_store = None
# login manager
login_manager = LoginManager()
login_manager.login_view = "user.login"
# jwt
jwt = JWTManager()


######################################
#### Application Factory Function ####
######################################
def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, 'api', 'client/templates'),
        static_folder=os.path.join(basedir, 'api', 'client/static'),
    )
    # get the .env config
    env = os.getenv("ENVIRONMENT") if os.getenv("ENVIRONMENT") is not None else "develop"
    config_class = config_map.get(env)
    app.config.from_object(config_class)

    logging_config_file = logging_config_file_map.get(env, None)
    if logging_config_file:
        with open(logging_config_file, "r") as logging_yaml:
            dictConfig(yaml.safe_load(logging_yaml.read()))

    initialize_extensions(app, config_class)
    register_blueprints(app)

    return app


##########################
#### Helper Functions ####
##########################
def initialize_extensions(app, config_class):
    # bind all extensions to the Flask application instance (app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # use flask-session to store session in redis
    Session(app)

    # set flask CSRF protection
    #CSRFProtect(app)

    # login manager
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    # jwt
    jwt.init_app(app)

    # Flask-Login configuration
    from api.server.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from api.server.user.view import user_blueprint
    app.register_blueprint(user_blueprint)

    from api.server.api_v2.controller import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api_v2/")
