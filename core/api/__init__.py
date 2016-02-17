import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions

from flask_pymongo import BSONObjectIdConverter
from core.api import settings
from core.api.models import db


def create_app(environment=None):
    """
    Create an app instance
    """
    app = Flask('core')
    app.url_map.converters['ObjectId'] = BSONObjectIdConverter

    # Config app for environment
    if not environment:
        environment = os.environ.get('BACKEND_ENVIRONMENT', 'Dev')

    app.config.from_object('core.api.settings.%s' % environment)

    # convert exceptions to JSON
    def make_json_error(ex):
        response = jsonify(
            message=str(ex)
        )
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    for code in default_exceptions.items():
        app.error_handler_spec[None][code] = make_json_error

    from core.api.views.endpoints import api
    app.register_module(api)

    # initialize modules
    db.init_app(app)

    return app
