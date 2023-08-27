#!/usr/bin/python3
""" objects that handle all default RestFul API actions for user_login """
from models.user import User
from models import storage
from flask import abort,current_app, Flask, jsonify, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
# from werkzeug.security import check_password_hash


app = Flask(__name__)

app.secret_key = "transhub_rosemary_joseph_samuel"
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    """
    Returns the home dashboard
    """
    return render_template("landing_page.html")


@app.teardown_appcontext
def tear_down(exception):
    """method to handle teardown"""
    storage.close


@app.errorhandler(404)
def not_found_error(error):
    """
    A handler for 404 errors
    """
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404



@login_manager.user_loader
def load_user(user_id):
    # Load and return the user object based on the user_id
    # This function is required by Flask-Login to retrieve users from the ID
    # It should return the user object or None if the user doesn't exist
    return storage.get(User, user_id)


@app.route('/login', methods=['POST'])
def login():
    """
    This If block manages the Post request when the user clicks submit
    after filling the html form
    """
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']

        """
        The session searches for the email address of the user
        to check if its in the database"""
        storage.reload()
        user = storage.get(User, email_address)
    
        if user is None or user.password != password:
            storage.close()
            error_message = "Invalid email or password"
            return redirect(url_for('home', error=error_message))
        else:
            login_user(user)
            storage.close()
            return render_template('home_page.html')


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    """
       Returns the profile of the user
       when the user clicks profile on the home page.
       The login_required decorator ensures that the user is loggedin
    """

    return render_template('user_login.html', user=current_user)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logs out user and return the login url"""
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":

    app.debug = True

    # Run the flask server
    app.run(host='0.0.0.0', port=5000, threaded=True)
