#!/usr/bin/python3
"""User API endpoint blue print"""
from flask import Blueprint, jsonify, abort
from models.user import User
from models import storage


user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/api/v1')

@user_blueprint.route('/users/', defaults={"user_attr": None})
@user_blueprint.route('/users/<user_attr>', strict_slashes=False)
def all_users(user_attr):
    """get users"""
    # return all users if no parameter is passed
    if user_attr is None:
        users = storage.all(User)
        return jsonify([item.to_dict() for item in users.values()])

    else:
        # serach for users for id first if parameter is passed
        user = storage.get(User, user_attr)
        if user is None:
            # search for user with email if id fails
            user = storage.get_email(User, user_attr)
        
        if user is None:
            # abort if both id and emails fails
            abort(404)
    return jsonify(user.to_dict())

@user_blueprint.route('/users/<user_attr>/wallet', strict_slashes=False)
def user_wallets(user_attr):
    """gets all wallets linked to this user"""
    # get user with id
    user = storage.get(User, user_attr)
    if user is None:
        # get user by email if id fails
        user = storage.get_email(User, user_attr)
        #if both id and email fails abort not found
        if user is None:
            abort(404)
    # if user has no wallet abort
    if user.wallet is None:
        abort(404)
    # return lists of wallets linked to the user
    return jsonify([item.to_dict() for item in user.wallet])

@user_blueprint.route('/users/<user_attr>/transactions', strict_slashes=False)
def user_transactions(user_attr):
    """gets all transactions linked to the user"""
    user = storage.get(User, user_attr)
    if user is None:
        user = storage.get_email(User, user_attr)
        if user is None:
            abort(404)
    if user.transactions is None:
        abort(404)
    return jsonify({'transactions': [item.to_dict() for item in user.transactions]})
