#!/usr/bin/python3
"""User API endpoint blue print"""
from flask import Blueprint, jsonify, abort, request
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

    results = {
            'transactions': [item.to_dict() for item in user.transactions]
            }
    return jsonify(results)

@user_blueprint.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """add a new user instance to database"""
    try:
        request.get_json()
    except Exception:
        abort(400, "Invalid JSON/No JSON data")
    if 'first_name' not in request.get_json():
        abort(400, "First name required")
    if 'last_name' not in request.get_json():
        abort(400, "Last name required")
    if 'email_address' not in request.get_json():
        abort(400, "Email address required")
    if 'phone_number' not in request.get_json():
        abort(400, "Phone number required")
    if 'address' not in request.get_json():
        abort(400, "Address required")
    if 'password' not in request.get_json():
        abort(400, "Password required")

    email = request.get_json().get('email_address')
    user = storage.get_email(User, email)
    if user:
        abort(400, "Email Exists")
    n_user = request.get_json()
    user = User(**n_user)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201

@user_blueprint.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user associated with user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    res = {
            'user_id': user_id,
            'delete': 'Yes'
            }
    return jsonify(res), 200

@user_blueprint.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update attribute of user associated with user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    try:
        request.get_json()
    except Exception:
        abort(400, "Invalid JSON/No JSON data")
    update = request.get_json()
    u_user = storage.update(user, update)

    return jsonify(u_user.to_dict()), 200

