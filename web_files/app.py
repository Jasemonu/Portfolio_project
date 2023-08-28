#!/usr/bin/python3
""" objects that handle all default RestFul API actions for user_login """
from models.user import User
from models import storage
from flask import abort,current_app, Flask, jsonify, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
# from werkzeug.security import check_password_hash


app = Flask(__name__)
""" A key to safely manage sessions for the flask app"""
app.secret_key = "transhub_rosemary_joseph_samuel"

login_manager = LoginManager(app)
"""The login_required decorator redirects here"""
login_manager.login_view = 'login'

storage.reload()

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Returns visitors page
    """
    return render_template("landing_page.html")


@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """Renders the user home page"""
    return render_template('home_page.html')


""" User Signup endpoint"""
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
    return redirect('index')


""" User Login Endpoint"""
@login_manager.user_loader
def load_user(user_id):
    # Load and return the user object based on the user_id
    # This function is required by Flask-Login to retrieve users from the ID
    # It should return the user object or None if the user doesn't exist
    return storage.get(User, user_id)


@app.route('/login', methods=['POST'], strict_slashes=False)
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
        print(user)
    
        if user is None or user.password != password:
            storage.close()
            error_message = "Invalid email or password"
            return redirect(url_for('index', error=error_message))
        else:
            login_user(user)
            storage.close()
            return render_template('wallet.html')


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
    return redirect(url_for('index'))


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
