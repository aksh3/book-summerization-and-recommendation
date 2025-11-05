import os
from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, ma
from flasgger import Swagger
from .routes import register_blueprints
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    ma.init_app(app)
    Swagger(app, template_file=os.path.join(os.path.dirname(__file__), "docs", "swagger.yaml"))
    register_blueprints(app)
    return app
