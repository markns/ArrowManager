# -*- coding: utf-8 -*-
"""The arrowmanager module, containing the arrowmanager factory function."""
from flask import Flask, render_template

from arrowmanager import commands, arrows
from arrowmanager import dashboard
from arrowmanager import public
from arrowmanager.assets import assets
from arrowmanager.extensions import cache, db, jwt, migrate, bcrypt, csrf_protect, CORS
from arrowmanager.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)

    # TODO: Read this https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    # TODO: And this: https://flask-cors.readthedocs.io/en/latest/
    CORS.init_app(app)
    # login_manager.init_app(app)
    # debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # stormpath_manager.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(dashboard.views.blueprint)
    app.register_blueprint(arrows.blueprint)

    # app.register_blueprint(auth)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_jwt_helpers(app):
    # app.jwt.user_claims_loader(auth.add_claims_to_access_token)
    # app.jwt.user_identity_loader(auth.user_identity_lookup_to_access_token)
    pass

def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'db': db
        }
        # 'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
