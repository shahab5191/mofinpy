import os
from dotenv import load_dotenv

from src.config import Config

load_dotenv('.env')


class TestConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    URL_PREFIX = '/api'
    ENVIRONMENT = 'test'
