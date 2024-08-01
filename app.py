"""
Entry point of the application.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask # type: ignore
from flask_smorest import Api # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from flask_migrate import Migrate # type: ignore
from flask import jsonify # type: ignore
from flask import render_template # type: ignore
from db import db
from resources.user import blp as UserBlp
from resources.patient import blp as PatientBlp
from resources.therapist import blp as TherapistBlp
from resources.app_request import blp as AppRequestBlp
from resources.app_response import blp as AppResponseBlp
from models import UserModel
from models import PatientModel
from models import TherapistModel
from models import AppRequestModel
from models import AppResponseModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app(db_url=None):
    app = Flask(__name__)

    # Configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Heartheal API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/api/docs"
    swagger_ui_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = swagger_ui_url
    database_uri = os.getenv("DATABASE_URL", "sqlite:///health.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_user_role_to_jwt(identity):
        # Here you can add roles based on your application's logic
        user = UserModel.query.get(identity)
        if user:
            return {"role": "user"}
        return {"role": None}

    def not_found(e):
        return jsonify({"code": 404, "status": "Not Found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"code": 405, "status": "Method Not Allowed"}), 405

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Server Error: {e}")
        return jsonify({"code": 500, "status": "Internal Server Error"}), 500

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "not-so-secret"

    # Register the blueprints
    api.register_blueprint(UserBlp, url_prefix='/users')
    api.register_blueprint(PatientBlp)
    api.register_blueprint(TherapistBlp)
    api.register_blueprint(AppRequestBlp)
    api.register_blueprint(AppResponseBlp)

    @app.route('/')
    def home():
        return render_template('index.html')
    @app.route('/about')
    def about():
        return render_template('about.html')
    @app.route('/service')
    def service():
        return render_template('service.html')
    
    @app.route('/dashboard')
    def dash():
        return render_template('dashj.html')

    @app.route('/consult')
    def consult():
        return render_template('consult.html')

    @app.route('/meditation')
    def meditation():
        return render_template('midt.html')

    @app.route('/mindfulness')
    def mindfulness():
        return render_template('mindfulness.html')

    @app.route('/groups')
    def groups():
        return render_template('groups.html')

    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
