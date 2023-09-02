#!/usr/bin/python3
"""wallet API endpoint blue print"""
from flask import Blueprint, abort, jsonify, request
from models.wallet import Wallet
from models.user import User
from models import storage


w_blueprint = Blueprint('w_blueprint', __name__, url_prefix='/api/v1')

@w_blueprint.route('/wallets/', defaults={'phone_number': None})
@w_blueprint.route('/wallets/<phone_number>', strict_slashes=False)
def all_wallet(phone_number):
    """get all wallet instances"""
    # return all instances if phone_number is None
    if phone_number is None:
        wallets = storage.all(Wallet)
        list_wallets =  [item.to_dict() for item in wallets.values()]
        return jsonify({'wallets': list_wallets})
    # search for instance base on wallet phone_number
    wallet = storage.wallet(Wallet, phone_number)
    # abort 404 if not found
    if wallet is None:
        abort(404)
    return jsonify({"wallet": wallet.to_dict()})

@w_blueprint.route('/wallets/<phone_number>/user', strict_slashes=False)
def wallet_user(phone_number):
    """return the user using the wallet with phone_number"""
    # search instance base on phone_number
    wallet = storage.wallet(Wallet, phone_number)
    # abort 404 if not found
    if wallet is None or wallet.user is None:
        abort(404)
    
    results = {
            'wallet': phone_number,
            'user': wallet.user.to_dict()
            }
    return jsonify(results)

@w_blueprint.route('/wallets/<phone_number>/transactions', strict_slashes=False)
def wallet_transactions(phone_number):
    """return all transactions linked to this wallet account"""
    # search instance base on phone_number
    wallet = storage.wallet(Wallet, phone_number)
    # abort 404 if not found
    if wallet is None or wallet.transactions is None:
        abort(404)
    results = {
            'wallet': wallet.phone_number,
            'transactions': [item.to_dict() for item in wallet.transactions]
            }
    return jsonify(results)

@w_blueprint.route('/wallets/<user_id>', methods=['POST'], strict_slashes=False)
def create_wallet(user_id):
    """Create new wallet for user associated with user_id"""
    try:
        request.get_json()
    except Exception:
        abort(400, "Invalid JSON/No JSON data")
    if 'phone_number' not in request.get_json():
        abort(400, "'phone number required")
    if 'pin' not in request.get_json():
        abort(400, "Pin required")
    if not storage.get(User, user_id):
        abort(404)
    if storage.wallet(Wallet, request.get_json().get('phone_number')):
        abort(400, "wallet exists")
    data = request.get_json()
    data['user_id'] = user_id
    wallet = Wallet(**data)
    storage.new(wallet)
    storage.save()
    return jsonify(wallet.to_dict()), 201

@w_blueprint.route('/wallets/<phone_number>', methods=['PUT'], strict_slashes=False)
def update_wallet(phone_number):
    """update the wallet associated with phone_number"""
    try:
        request.get_json()
    except Exception:
        abort(400, "Invalid JSON/No JSON data")
    wallet = storage.wallet(Wallet, phone_number)
    if wallet is None:
        abort(404)
    data = request.get_json()
    u_wallet = storage.update(wallet, data)
    return jsonify(u_wallet.to_dict()), 200

@w_blueprint.route('/wallets/<phone_number>', methods=['DELETE'], strict_slashes=False)
def delete_wallet(phone_number):
    """delete the wallet associated with phone_number"""
    wallet = storage.wallet(Wallet, phone_number)
    if wallet is None:
        abort(404)
    storage.delete(wallet)
    storage.save()
    res = {
            'wallet_number': phone_number,
            'deleted': 'Yes'
            }
    return jsonify(res), 200
