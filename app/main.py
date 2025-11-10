# app/main.py
import os

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request
from .config import Config
from .extensions import db, migrate, jwt, ma
from flasgger import Swagger
from .routes import register_blueprints, reviews_bp, books_bp
from flask_cors import CORS
from flasgger import Swagger

from .extensions import (
    db,
    migrate,
    jwt,
    ma,
    init_async_db,
)
from .config import Config
from .routes.auth import auth_bp
from .services.recommendation_and_generateSummery import generate_summary, get_recommendations_for_user
from .utils.jwt_utils import jwt_required


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(reviews_bp, url_prefix="/books")

    # app.register_blueprint(summaries_bp, url_prefix="/summaries")
    # app.register_blueprint(recs_bp, url_prefix="/recommendations")

    @app.route("/")
    def api_root():
        return {"msg": "Welcome to Bookman API. See /apidocs for Swagger."}, 200

    @app.route("/generate-summary", methods=["POST"])
    @jwt_required()
    async def generate():
        data = request.get_json()
        return await generate_summary(data)

    @app.route("/recommendations", methods=["GET"])
    @jwt_required()
    async def recommendations():
        args = request.args
        return await get_recommendations_for_user(args)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Sync DB
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    CORS(app, supports_credentials=True)

    # ✅ Initialize Async DB AFTER config is loaded
    async_url = app.config["ASYNC_DATABASE_URI"]
    print("[create_app] Initializing async DB with:", async_url)
    init_async_db(async_url)

    Swagger(app, template_file=os.path.join(os.path.dirname(__file__), "docs", "swagger.yaml"))

    register_blueprints(app)
    return app
