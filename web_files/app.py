#!/usr/bin/python3
"""Script create a folder"""

from flask import Flask, jsonify, render_template, request
from flask import redirect
from models import storage
from models.user import User
from api.v1.views import app_views
# from flask_login import LoginManager


app = Flask(__name__)
""" A key to safely manage sessions for the flask app"""
# app.secret_key = "transhub_rosemary_joseph_samuel"

# login_manager = LoginManager(app)
"""The login_required decorator redirects here"""
# login_manager.login_view = 'login'

app.register_blueprint(app_views)
storage.reload()

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Returns visitors page
    """
    return render_template("landing_page.html")

@app.route('/signup', methods=["POST"], strict_slashes=False)
def sign_up():
    """Sign user up """
    n_user = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email_address': request.form.get('email_address'),
            'phone_number': request.form.get('phone_number'),
            'gender': request.form.get('gender'),
            'address': request.form.get('address'),
            'password': request.form.get('password')
            }
    if request.form.get('password') == request.form.get('confirm_password'):
        userObject = User(**n_user)
        storage.new(userObject)
        storage.save()

        return userObject.to_dict()
    return redirect('/')

@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """Renders the user home page"""
    return render_template('home_page.html')

@app.route('/signin', methods=["POST"], strict_slashes=False)
def sing_in():
    """Signs a user in by checking the passwor and eamil"""
    email = request.form.get('email_address')
    password = request.form.get('password')

    user = storage.get(User, email)
    if password == user.to_dict().get('password'):
        return redirect('/home')
    return "Invaled email or password"

@app.teardown_appcontext
def tear_down(Exception):
     """method to handle teardown"""
     storage.close()

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
