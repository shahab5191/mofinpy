def get_toekn_from_cookie(cookie):
    token = cookie[cookie.index("=") + 1:]
    return token
