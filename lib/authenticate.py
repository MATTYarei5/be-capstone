import functools
from datetime import datetime
from uuid import UUID

from flask import request, jsonify

from db import db
from models.auth import Auth


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except:
        return False


def validate_token(arg_zero):
    auth_token = arg_zero.headers['auth']

    if not auth_token or not validate_uuid4(auth_token):
        return False

    existing_token = db.session.query(Auth).filter(Auth.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now():
            return existing_token
    else:
        return False


def fail_response():
    return jsonify({"message": "authentication required"}), 401


def auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(request)

        return (
            func(
                *args, **kwargs
            ) if auth_info else fail_response()
        )
    return wrapper_auth_return


def authenticate_return_auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(request)
        kwargs['auth_info'] = auth_info

        return (
            func(
                *args, **kwargs
            ) if auth_info else fail_response()
        )
    return wrapper_auth_return
