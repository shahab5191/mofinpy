from datetime import datetime, timedelta
from flask import jsonify, request, make_response
from src.config import Config
from src.models.user import User
from src.users import bp
from marshmallow import Schema, fields, ValidationError, validate
import jwt
from src.utils import get_toekn_from_cookie

from src.utils.encryption import validate_token


class SignSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=20)
    )


@bp.route('/users/current')
def users():
    json_data = request.json
    if not json_data or 'jwt' not in json_data:
        return {"err": "you are not logged in!"}, 403

    token = json_data['jwt']

    payload = validate_token(token)
    if not payload:
        return {"err": "You are not logged in!"}, 403

    return payload


@bp.route('/users/refreshtoken')
def refresh_token():
    cookie = request.headers['Cookie']
    token = get_toekn_from_cookie(cookie)

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return {"msg": "You are not logged in!"}, 403

    try:
        new_token = jwt.encode(
            {
                "id": payload['id'],
                "exp": datetime.utcnow() + timedelta(hours=1)
            },
            Config.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as err:
        print(err)
        return {"msg": "Somthing went wrong! please try again later"}, 500

    response = make_response({"msg": "Token refreshed!"})
    response.set_cookie('token',
                        new_token,
                        expires=datetime.utcnow() + timedelta(hours=1)
                        )
    return response


@bp.route('/users/signup', methods=["POST"])
def signup():
    json_data = request.json
    if not json_data:
        return {"err": "You must provide email and password!"}, 400
    schema = SignSchema()
    try:
        schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        createUserResponse = User(
            email=json_data['email'],
            password=json_data['password']
        ).json()
    except Exception as err:
        return {"err": str(err)}, 400

    if not createUserResponse:
        return {"err": "somthing went wrong!"}, 500

    return createUserResponse, 201


@bp.route('/users/signin', methods=["POST"])
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
        user = User.getUser(email, password)
    except Exception:
        return {"err": "email or password is not valid!"}, 403

    try:
        token = jwt.encode(
            payload={'id': str(user.id)},
            key=Config.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as err:
        print(err)
        return {"err": "Somthing went wrong! please try again later"}, 500

    response = make_response({"msg": "You logged in successfully"})
    response.set_cookie(
        'token',
        token,
        expires=datetime.utcnow() + timedelta(hours=1)
    )
    return response
