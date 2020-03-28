class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    SQLACHEMY_ECHO = False
    SECRET_KEY = 'PROD'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'DEV'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
