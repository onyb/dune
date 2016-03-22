import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import BSONObjectIdConverter, PyMongo
from werkzeug.exceptions import HTTPException, default_exceptions

from core.api import settings
from core.api.models import mongo_client


def create_app(environment=None):
    """
    Create an app instance
    """
    app = Flask('core')

    # Allow CORS for all domains on all routes
    CORS(app)

    mongo_client = PyMongo(app)

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
    mongo_client.init_app(app)

    return app
