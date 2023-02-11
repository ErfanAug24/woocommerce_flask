import datetime
import os
from dotenv import load_dotenv


class Config(object):
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    PROPAGATE_EXCEPTIONS = os.getenv('PROPAGATE_EXCEPTIONS')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
