import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465  # This is typically the SSL port for Gmail
    MAIL_USE_SSL = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://newuser:kiki@localhost:5432/serene'
    DEBUG = True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

config_options = {
    'development': DevelopmentConfig,
    'production': ProdConfig,
    'default': DevelopmentConfig
}
