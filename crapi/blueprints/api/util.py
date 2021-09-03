from functools import wraps
from hmac import compare_digest

from flask import current_app, request
from flask_restful import abort


def authenticate_bot(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        known_key = current_app.config.get('OOERBOT_API_KEY')
        given_key = request.headers.get('X-API-Key', '')

        if compare_digest(known_key, given_key):
            return func(*args, **kwargs)

        abort(401)

    return wrapper
