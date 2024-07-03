from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask.cli import ScriptInfo
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
mail = Mail()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    # Debug print statements
    print(f"Initial config_name: {config_name}")
    print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
    print(f"FLASK_CONFIG: {os.environ.get('FLASK_CONFIG')}")

    # Handle ScriptInfo object
    if isinstance(config_name, ScriptInfo):
        config_name = None

    # If config_name is None, try to get it from environment variables
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    print(f"Final config_name: {config_name}")
    print(f"Available config_options: {list(config_options.keys())}")

    app.config.from_object(config_options[config_name])

    # Initializing extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Registering blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
