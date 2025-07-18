from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    """Função que cria e configura a aplicação Flask."""
    app = Flask(__name__)
    
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 280
    }

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.models import User

    return app