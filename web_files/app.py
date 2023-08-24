#!/usr/bin/python3
"""Script create a folder"""

from flask import Flask, jsonify, render_template
# from models import storage
from api.v1.views import app_views
# from flask_login import LoginManager


app = Flask(__name__)
""" A key to safely manage sessions for the flask app"""
# app.secret_key = "transhub_rosemary_joseph_samuel"

# login_manager = LoginManager(app)
"""The login_required decorator redirects here"""
# login_manager.login_view = 'login'

app.register_blueprint(app_views)


@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    """
    Returns the home dashboard
    """
    return render_template("landing_page.html")

'''
@app.teardown_appcontext
def tear_down(exception):
    """method to handle teardown"""
    storage.close()
'''

@app.errorhandler(404)
def not_found_error(error):
    """
    A handler for 404 errors
    """
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404


@app.errorhandler(400)
def invalid_login(error):
    response = "Invalid email or password"
    return jsonify(response), 400


if __name__ == "__main__":

    app.debug = True

    # Run the flask server
    app.run(host='0.0.0.0', port=5000, threaded=True)
