#!/usr/bin/python3
"""wallet API endpoint blue print"""
from flask import Blueprint, abort, jsonify
from models.wallet import Wallet
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
