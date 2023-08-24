#!/usr/bin/python3
""" objects that handle all default RestFul API actions for user_login """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from api.v1.app import app, login_manager
from werkzeug.security import check_password_hash

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app_views.route('/login', methods=['GET', 'POST'])
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
        session.close()
        return redirect(url_for('home'))
    else:
        session.close()
        abort(400)

    """
    The GET request that renders the form tag in the login html template
    for users to fill"""
    return render_template('login.html')


@app_views.route('/profile', methods=['GET'])
@login_required
def profile():
    """
       Returns the profile of the user
       when the user clicks profile on the home page.
       The login_required decorator ensures that the user is loggedin
    """

    return render_template('profile.html', user=current_user)


@app_views.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logs out user and return the login url"""
    logout_user()
    return redirect(url_for('login'))
