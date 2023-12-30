from datetime import datetime, timedelta
from flask import jsonify, request, make_response
from src.config import Config
from src.users import bp
from src.users.functions import create_user, getUser
from marshmallow import Schema, fields, ValidationError, validate
import jwt

from src.utils.encryption import generate_token, validate_token


class SignSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=20)
    )


@bp.route('/api/users/current')
def users():
    authHeader = request.headers.get('Authorization')
    if authHeader is None:
        return {"err": "You are not logged in!"}, 401

    token = authHeader[authHeader.index(" ") + 1:]
    if token is None:
        return {"err": "please provide previous token"}, 400

    payload = validate_token(token)
    if not payload:
        return {"err": "You are not logged in!"}, 401

    return payload


@bp.route('/api/users/refreshtoken')
def refresh_token():
    authHeader = request.headers.get('Authorization')
    if authHeader is None:
        return {"err": "please provide token"}

    token = authHeader[authHeader.index(" ") + 1:]
    if token is None:
        return {"err": "please provide previous token"}

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return {"msg": "You are not logged in!"}, 401

    new_token = generate_token(payload['id'], payload['email'])
    if new_token is None:
        return {"msg": "Somthing went wrong! please try again later"}, 500

    response = make_response({"msg": "Token refreshed!"})
    response.set_cookie('token',
                        new_token,
                        expires=datetime.now(UTC) + timedelta(hours=1)
                        )
    return response


@bp.route('/api/users/signup', methods=["POST"])
def signup():
    json_data = request.json
    if not json_data:
        return {"err": "You must provide email and password!"}, 400
    schema = SignSchema()
    try:
        schema.load(json_data)
    except ValidationError as err:
        print('[signup_route]', err)
        return jsonify(err.messages), 400

    try:
        createUserResponse = create_user(
            email=json_data['email'],
            password=json_data['password']
        ).json()
    except Exception as err:
        print('[signup_route]', err)
        return {"err": str(err)}, 400

    if not createUserResponse:
        return {"err": "somthing went wrong!"}, 500

    return createUserResponse, 201


@bp.route('/api/users/signin', methods=["POST"])
def signin():
    json_data = request.json

    if not json_data:
        return {"err": "You must provide email and password!"}, 400
    schema = SignSchema()
    try:
        schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    email = json_data["email"]
    password = json_data["password"]

    try:
        user = getUser(email, password)
    except Exception:
        return {"err": "email or password is not valid!"}, 401

    token = generate_token(str(user.id), user.email)

    if token is None:
        return {"err": "Somthing went wrong! please try again later"}, 500

    response = make_response({"msg": "You logged in successfully"})
    response.set_cookie(
        'token',
        token,
        expires=datetime.now(UTC) + timedelta(hours=1)
    )
    return response
