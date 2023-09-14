#!/usr/bin/python3
""" objects that handle all default RestFul API actions for user_login """
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction
from models import storage
from flask import abort,current_app, Flask, jsonify, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user, LoginManager

# Instantiation of app
app = Flask(__name__)

# A key to safely manage sessions for the flask app
app.secret_key = "transhub_rosemary_joseph_samuel"

# Instatiation of Login Manger with instance of our app
login_manager = LoginManager(app)

# The login_required decorator redirects here
login_manager.login_view = 'login'

# Creating a session and re-loading data from database
storage.reload()


# default route
@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Returns visitors page
    """
    return render_template("landing_page.html")

# Home page route
@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """Renders the user home page"""
    return render_template('home_page.html')


# User Signup endpoint
@app.route('/signup', methods=["POST"], strict_slashes=False)
def sign_up():
    """Sign user up """
    users = storage.all(User)
    for item in users.values():
        if item.email_address == request.form.get('email_address'):
            flash('Email already exists')
            return redirect(url_for('index'))
    # creating new user dictionary from form attributes
    new_user = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email_address': request.form.get('email_address'),
        'phone_number': request.form.get('phone_number'),
        'gender': request.form.get('gender'),
        'address': request.form.get('address'),
        'password': ''
        }

    # check if password is same in comfirm password
    if request.form.get('password') == request.form.get('confirm_password'):
        get_password = request.form.get('password')
        # hash password before saving in database
        hashed_password = generate_password_hash(get_password, method='MD5')
        new_user['password'] = hashed_password
        # create the user 
        userObject = User(**new_user)
        # add to session
        storage.new(userObject)
        # commit to database
        storage.save()
        # return to landing page and flash Signup successfull
        flash("Signup successfull please Login")
        return redirect(url_for('index'))
    # if password mismatch, return user to landing page 
    flash('Please check password and Try agian')
    return redirect(url_for('index'))

# Load user details base on id passed to load_user
@login_manager.user_loader
def load_user(user_id):
    """
    Load and return the user object based on the user_id
    This function is required by Flask-Login to retrieve users from the ID
    It should return the user object or None if the user doesn't exist
     """
    return storage.get(User, user_id)

# Log in endpoint
@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    This If block manages the Post request when the user clicks submit
    after filling the html form
    """
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']

        # The session searches for the email address of the user
        # to check if its in the database
        user = storage.get_email(User, email_address)
        if user is None:
            flash("User doesn't exist")
            return redirect(url_for('index'))
        get_password = check_password_hash(user.password, password)
    
        if not get_password:
            storage.close()
            flash("Invalid email or password")
            return redirect(url_for('index'))
        else:
            login_user(user)
            storage.close()
            flash("Login Successful")
            return render_template('home_page.html')


# user profile endpoint
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    """
       Returns the profile of the user
       when the user clicks profile on the home page.
       The login_required decorator ensures that the user is loggedin
    """

    return render_template('user_login.html', user=current_user)

# log out endpoint
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logs out user and return the login url"""
    logout_user()
    flash("Logged Out")
    return redirect(url_for('index'))


# transfer enpoint
@app.route('/transfers/wallet', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def transfer():
    """User saving, transfer or taking money from account"""
    for item in current_user.wallet:
        wallet_id = item.id
        balance = item.balance
        pin = item.pin
    data = {
            'user_id': current_user.id,
            'wallet_id': wallet_id,
            'recipient_account': request.form.get('wallet_number'),
            'amount': request.form.get('amount'),
            'transaction_type': 'transfer',
            'description': request.form.get('description'),
            'status': 'pending'
            }
        
    get_pin = request.form.get('pin')
    if int(get_pin) == pin:
        status = transfer(data, balance, wallet_id)
        if status == '1':
            flash('Transfer successfull')
            return redirect(url_for('dashboard'))
        elif status == '2':
            flash('Insufficient Balance')
            return redirect(url_for('dashboard'))
        else:
            flash("Wallet doesn't exists")
            return redirect(url_for('dashboard'))
    flash('Invalid PIN number')
    return redirect(url_for('dashboard'))


# function to call for transfer endpiont
def transfer(data, acb, id):
    """send money from wallet to another wallet"""
    receiver = storage.wallet(Wallet, data['recipient_account'])
    # check if sender id is not same as receiver id
    if receiver.id == id:
        # return 3 for wallet does ot exists
        return '3'
    # check if receiver exists 
    if receiver:
        # get receiver full name
        name = receiver.user.first_name +' ' + receiver.user.last_name
        # update receiver name in data
        data['recipient_name'] = name
        # get sender wallet base on id
        wallet_obj = storage.get(Wallet, id)
        # loop through user wallet relationship to get wallet infomation
        for item in current_user.wallet:
            sender_account = item.phone_number
        # sender full name
        sender_name = current_user.first_name + ' ' + current_user.last_name
        # receiver transaction details
        receiver_data = {
                'user_id': receiver.user.id,
                'wallet_id': receiver.id,
                'sender_account': sender_account,
                'sender_name': sender_name,
                'amount': '',
                'transaction_type': 'credit',
                'description': data.get('description'),
                'status': 'pending'
                }

        # check if sender have enough balance then continue
        if acb >= float(data['amount']):
            # subtract the transaction amount from balance
            balance = acb - float(data['amount'])
            # sender transaction object
            sender_trans = Transaction(**data)
            # receiver data with the amount debited
            receiver_data['amount'] = data['amount']
            # receiver transaction object
            receiver_trans = Transaction(**receiver_data)
            # credit receiver with the transaction amount
            receiver_balance = receiver.balance + float(receiver_trans.amount)
            # add objects to session
            storage.new(sender_trans)
            storage.new(receiver_trans)
            # update the objects in database and save
            storage.update(wallet_obj, {'balance': balance})
            storage.update(receiver, {'balance': receiver_balance})
            storage.update(sender_trans, {'status': 'approved'})
            storage.update(receiver_trans, {'status': 'approved'})
            # return 1 for trasaction successful
            return '1'
        else:
            # return 2 if balance is not enough
            return '2'
        # return 3 if receiver does not exists
    return '3'


# wallet creation endpoint
@app.route('/create-wallet', methods=['GET', 'POST'], strict_slashes=False)
def create_wallet():
    """Retrieve data from the request"""
    phone_number = request.form.get('phone_number')
    next_of_kin = request.form.get('next_of_kin')
    next_of_kin_relationship = request.form.get('next_of_kin_relationship')
    next_of_kin_number = request.form.get('next_of_kin_number')
    pin = request.form.get('pin')
    confirm_pin = request.form.get('confirm_pin')
    
    """wallet validation checks"""
    if pin is None or confirm_pin is None:
        flash('Pin numbers must be provided')
        return redirect(url_for('home'))
        
    if pin != confirm_pin:
        flash('Pin numbers do not match')
        return redirect(url_for('home'))

    if len(pin) < 4:
        flash('Pin should be at least 4 characters')
        return redirect(url_for('home'))

    """Check if the same phone number is being used"""
    storage.reload()
    wallet = storage.wallet(Wallet, phone_number)
    if wallet:
        storage.close()
        flash('This phone number already exist')
        return redirect(url_for('dashboard'))
    else:
       # if current_user.has_wallet:
        if current_user.is_authenticated and current_user.wallet:
            storage.close()
            flash('You already have a wallet')
            return redirect(url_for('dashboard'))

        """If the user does not have a wallet, proceed to create one"""
        new_wallet = {
            'user_id': current_user.id,
            'phone_number': phone_number,
            'next_of_kin': next_of_kin,
            'next_of_kin_relationship': next_of_kin_relationship,
            'next_of_kin_number': next_of_kin_number,
            'pin': pin
        }
        wallet = Wallet(**new_wallet)
        storage.new(wallet)
        storage.save()
        flash('Wallet created successfully.', 'success')
        return redirect(url_for('dashboard'))


# wallet dashboard
@app.route('/dashboard', strict_slashes=False)
def dashboard():
    """This ensures that users without wallet cannot access the dashboard page"""
    #if current_user.has_wallet == True:
    if current_user.is_authenticated and current_user.wallet:
        return render_template('wallet.html')
    flash('Please you have no wallet, kindly create one')
    return redirect(url_for('home'))

# close data on exit from app
@app.teardown_appcontext
def tear_down(Exception):
     """method to handle teardown"""
     storage.close()
# error handler
@app.errorhandler(404)
def not_found_error(error):
    """
    A handler for 404 errors
    """
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404


# error handler
@app.errorhandler(400)
def invalid_login(error):
    response = "Invalid email or password"
    return jsonify(response), 400

# app start from here
if __name__ == "__main__":

    app.debug = True

    # Run the flask server
    app.run(host='0.0.0.0', port=5000, threaded=True)
