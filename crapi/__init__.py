import click
from flask import Flask
from flask_session import Session
from flask_wtf import CSRFProtect


def create_app(config_override=None):
    application = Flask(__name__, instance_relative_config=True)

    application.config.from_pyfile('config.py')
    application.config.from_object(config_override)

    Session(application)
    CSRFProtect(application)

    from crapi.models import db
    db.init_app(application)

    from crapi.data import ma
    ma.init_app(application)

    from crapi.blueprints.auth import login_manager
    login_manager.init_app(application)

    from crapi import blueprints
    for blueprint in blueprints.blueprints:
        application.register_blueprint(blueprint)

    @application.cli.command()
    def routes():
        for rule in application.url_map.iter_rules():
            click.echo("%s %s" % (rule, rule.endpoint))

    return application
