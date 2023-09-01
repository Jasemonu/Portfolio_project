#!/usr/bin/python3
"""Setting up app to run from created blueprints of our endpoints"""
from flask import Flask, jsonify
from models import storage
from api.v1.views.user import user_blueprint
from api.v1.views.wallet import w_blueprint
from api.v1.views.transaction import trans_blueprint


def create_app():
    """A function to create and return our app instance"""
    app = Flask(__name__)

    # blueprint for user api endpoint
    app.register_blueprint(user_blueprint)

    # blue print for wallet api endpoints
    app.register_blueprint(w_blueprint)

    # blueprint for transaction api endpoints
    app.register_blueprint(trans_blueprint)

    @app.route('/api/v1/status', strict_slashes=False)
    def status():
        """resturn status of api"""
        status = {'Status': 'OK'}

        return jsonify(status)

    @app.errorhandler(404)
    def not_found(error):
        """404 handler"""
        _404 = {"404": "Not Found"}

        return jsonify(_404)

    with app.app_context():
        storage.reload()

    @app.teardown_appcontext
    def close_storage(Exception):
        """close database sessions created in app"""
        storage.close()

    return app
