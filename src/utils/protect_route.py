from functools import wraps
from flask import g, request
from src.utils.encryption import validate_token


def protected_route(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return error_401()

        token = request.headers['Authorization']
        token = token[token.index(" ") + 1:]
        decoded_token = validate_token(token)
        if not decoded_token:
            return error_401()
        g.user_data = {
            'id': decoded_token['id'],
            'email': decoded_token['email']}
        return func(*args, **kwargs)
    return wrapper_func


def error_401():
    return {"err": "You are not authorized to do this action!"}, 401
