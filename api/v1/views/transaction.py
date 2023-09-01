#!/usr/bin/python3
"""transaction API endpoints blue print"""
from flask import Blueprint, abort, jsonify
from models.transaction import Transaction
from models import storage


trans_blueprint = Blueprint('trans_blueprint', __name__, url_prefix='/api/v1')

@trans_blueprint.route('/transactions/', defaults={'id': None})
@trans_blueprint.route('/transactions/<id>', strict_slashes=False)
def all_transactions(id):
    """return all instance of transactions"""
    # return all instances if id is None
    if id is None:
        trans = storage.all(Transaction)
        return jsonify([item.to_dict() for item in trans.values()])

    # search for instace based on id
    trans = storage.get(Transaction, id)
    # abort 404 if not found
    if trans is None:
        abort(404)

    return jsonify(trans.to_dict())

@trans_blueprint.route('/transactions/<id>/wallet', strict_slashes=False)
def transaction_wallet(id):
    """return the wallet linked to the transaction with id"""
    # search instance base on id
    trans = storage.get(Transaction, id)
    # abort 404 if not found
    if trans is None:
        abort(404)
    results = {
            'transaction_id': id,
            'wallet': trans.wallet.to_dict()
            }
    return jsonify(results)

@trans_blueprint.route('/transactions/<id>/user', strict_slashes=False)
def transaction_user(id):
    """return the user linked to the transaction with id"""
    # search instance base on id
    trans = storage.get(Transaction, id)
    # abort 404 if not found
    if trans is None:
        abort(404)
    results = {
            'transaction_id': id,
            'user': trans.user.to_dict()
            }
    return jsonify(results)
