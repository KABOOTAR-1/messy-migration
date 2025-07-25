from flask import Flask
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)

    from .config import Config
    app.config.from_object(Config)
    
    JWTManager(app)

    from .auth.routes import auth_bp
    from .api.routes import api_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    from .models.user_model import init_db
    with app.app_context():
        init_db()

    return app