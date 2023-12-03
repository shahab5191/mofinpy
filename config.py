import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_SECRET = os.environ.get('JWT_SECRET')
    DB_URL = os.environ.get('DB_URL')
