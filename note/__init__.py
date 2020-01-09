# -*- coding: utf-8 -*-

import importlib

from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager

from note.extensions import db
from note.models.user import Users
from note.urls import routers


def load_config_class(config_name):
    """导入config配置"""
    config_class_name = "%sConfig" % config_name.capitalize()
    app_name = __name__
    mod = importlib.import_module('%s.config.%s' % (app_name, config_name))
    config_class = getattr(mod, config_class_name, None)
    return config_class


def create_app(config_name):
    """创建app"""
    app = Flask(__name__)
    config_class = load_config_class(config_name)
    app.config.from_object(config_class)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_blueprint(app)
    configure_loginmanager(app)
    return app


def configure_loginmanager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    @login_manager.user_loader
    def load_user(user_id):
        user = Users.query.filter(Users.id == user_id).first()
        if user:
            return user
        else:
            return None


def configure_blueprint(app):
    for blueprint, url_prefix in routers:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_extensions(app):
    db.init_app(app)


def configure_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(
            "errors/{0}.html".format(error_code),
            error=error
        ), error_code

    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
