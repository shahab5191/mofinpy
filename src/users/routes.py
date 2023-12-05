from src.users import bp


@bp.route('/users/')
def users():
    return {"msg": "users"}


@bp.route('/users/signup')
def signup():
    return {"msg": "sign up"}


@bp.route('/users/signin')
def signin():
    return {"msg": "sign in"}
