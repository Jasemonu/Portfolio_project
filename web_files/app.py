#!/usr/bin/python3
""" objects that handle all default RestFul API actions for user_login """
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.wallet import Wallet
from models import storage
from flask import abort,current_app, Flask, jsonify, render_template, redirect, url_for, request, flash
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
    users = storage.all(User)
    for item in users.values():
        if item.email_address == request.form.get('email_address'):
            flash('Email already exists')
            return redirect(url_for('index'))

    n_user = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email_address': request.form.get('email_address'),
        'phone_number': request.form.get('phone_number'),
        'gender': request.form.get('gender'),
        'address': request.form.get('address'),
        'password': ''
        }

    if request.form.get('password') == request.form.get('confirm_password'):
        get_password = request.form.get('password')
        hashed_password = generate_password_hash(get_password, method='sha256')
        n_user['password'] = hashed_password
        userObject = User(**n_user)
        storage.new(userObject)
        storage.save()

        return redirect(url_for('home'))
    return redirect('index')

""" User Login Endpoint"""
@login_manager.user_loader
def load_user(user_id):
    # Load and return the user object based on the user_id
    # This function is required by Flask-Login to retrieve users from the ID
    # It should return the user object or None if the user doesn't exist
    return storage.get(User, user_id)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
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
        user = storage.get_email(User, email_address)
        get_password = check_password_hash(user.password, password)
    
        if user is None or get_password is None:
            storage.close()
            error_message = "Invalid email or password"
            return redirect(url_for('index', error=error_message))
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
    return redirect(url_for('index'))

@app.route('/transaction', methods=['POST'], strict_slashes=False)
@login_required
def transaction():
    """User saving, transfer or taking money from account"""
    for item in current_user.wallet:
        wallet_id = item.id
        balance = item.account_balance
    trans = {
            'user_id': curent_user.id,
            'wallet_id': wallet_id,
            'recipient_name': request.form.get('recipient_name'),
            'recipient_account': request.form.get('recipient_account'),
            'amount': request.form.get('amount'),
            'transaction_type': request.form.get('transaction_type'),
            'description': request.form.get('description'),
            'status': 'pending'
            }
    trans_obj = Transaction(**trans)
    storage.new(trans_obj)
    storage.save()
    if trans_obj.transaction_type != 'transfer':
        ret =  deposite(trans_obj, balance)
        if ret:
            flash(ret + 'successful')
            return redirect(url_for('dasboard'))
        flash('transaction unsuccessful')
        return redirect(url_for('dasboard'))
    ret = transfer(trans_obj, balance, wallet_id)
    if ret:
        flash(ret + 'successful')
        return redirect(url_for('dashbaord'))
    flash('transaction unsuccessful')
    return redirect(url_for('dashboard'))

def deposit(cls, acb):
    """top up user balance"""
    if cls is None:
        return None
    wallet = storage.wallet(Wallet, cls.recipient_account)
    if cls.transaction_type == 'deposite':
        balance = acb + cls.amount
        storage.update(wallet, {'account_balnce': balance})
        storage.update(cls, {'status': 'approved'})
        return 'deposite'
    if cls.transaction_type == 'widrawal':

        if cls.amount > acb:
            return None
        balance = acb - csl.amount
        storage.update(wallet, {'account_balnce': balance})
        storage.update(cls, {'status': 'approved'})
    return 'widrawal'

def transfer(cls, acb, id):
    """send money from wallet to another wallet"""
    if  cls is None:
        return None
    reciever = storage.wallet(Wallet, cls.recipient_account)
    if reciever:
        wallet = storage.all(Wallet)
        for item in wallet.values():
            if item.id == id:
                wallet_obj = item

        if acb >= cls.amount:
            balance = acb - cls.amount
            storage.update(wallet_obj, {'account_balnce': balance})
            storage.update(cls, {'status': 'approved'})
            return True
        else:
            return None
    else:
        return None

@app.route('/create-wallet', methods=['GET', 'POST'], strict_slashes=False)
def create_wallet():
    """Retrieve data from the request"""
    phone_number = request.form.get('phone_number')
    next_of_kin = request.form.get('next_of_kin')
    next_of_kin_number = request.form.get('next_of_kin_number')
    pin = request.form.get('pin')
    confirm_pin = request.form.get('confirm_pin')
    
    """wallet validation checks"""
    if pin is None or confirm_pin is None:
        flash('Pin numbers must be provided')
        print('i noticed an error')
        
    if pin != confirm_pin:
        flash('Pin numbers do not match')
        return render_template('form.html')

    if len(pin) < 4:
        flash('Pin should be at least 4 characters')
        return render_template('form.html')

    """Check if the same phone number is being used"""
    storage.reload()
    wallet = storage.wallet(Wallet, phone_number)
    if wallet:
        storage.close()
        flash('This phone number has already been used for a wallet')
        return render_template('form.html')
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
            'next_of_kin_number': next_of_kin_number,
            'pin': pin
        }
        wallet = Wallet(**new_wallet)
        storage.new(wallet)
        storage.save()
        flash('Wallet created successfully.', 'success')
        return redirect(url_for('dashboard'))


@app.route('/dashboard', strict_slashes=False)
def dashboard():
    """This ensures that users without wallet cannot access the dashboard page"""
    #if current_user.has_wallet == True:
    if current_user.is_authenticated and current_user.wallet:
        return render_template('wallet.html')
    flash('Please you have no wallet, kindly create one')
    return redirect(url_for('home'))


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
