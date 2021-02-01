# importing modules
from functools import wraps
from flask import session, flash, redirect, url_for, request, jsonify
import re
from abbrefy.users.models import User


# login in required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'current_user' in session:
            if session['is_authenticated'] and "current_user" in session:
                user = session['current_user']

        else:
            flash('You must be signed in to access that page', 'danger')
            return redirect(url_for('users.signin'))

        return f(user, *args, **kwargs)

    return decorated


# login in required decorator
def no_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'is_authenticated' in session:
            if session["is_authenticated"] == True:
                return redirect(url_for('users.dashboard', username=session['current_user']['username']))

        return f(*args, **kwargs)

    return decorated


# login in required decorator
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not "apiKey" in request.headers:
            return jsonify({"status": False, "error": "Please provide your API key."})

        apiKey = request.headers.get('apiKey')

        user = User.get_key_owner(apiKey)

        if not user:
            return jsonify({"status": False, "error": "Invalid API key provided."})

        return f(user, *args, **kwargs)

    return decorated


# helper function for validating username
def validate_username(username):
    validator = "^[a-zA-Z0-9_]+$"
    validated = re.match(validator, username)
    if not validated:
        return False
    return True
