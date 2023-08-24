#!/usr/bin/python3
""" objects that handle all default RestFul API actions for user_login """
from models.user import User
from models import storage
from flask import abort, Flask, jsonify, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from werkzeug.security import check_password_hash


app = Flask(__name__)

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


@login_manager.user_loader
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This If block manages the Post request when the user clicks submit
    after filling the html form
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    """
    The session searches for the email address of the user
    to check if its in the database"""
    user = session.query(User).filter_by(email=email).first()

    """
    The user password is checked against the hashed password table
    which was created during registration
    """
    if user and check_password_hash(user.password, password):
        login_user(user)
        storage.close()
        return redirect(url_for('home'))
    else:
        storage.close()
        abort(400)

    """
    The GET request that renders the form tag in the login html template
    for users to fill"""
    return render_template('login.html')


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    """
       Returns the profile of the user
       when the user clicks profile on the home page.
       The login_required decorator ensures that the user is loggedin
    """

    return render_template('profile.html', user=current_user)


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
