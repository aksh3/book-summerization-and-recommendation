from flask import request

from .auth import auth_bp
from .books import books_bp
from .reviews import reviews_bp
from ..services.recommendation_and_generateSummery import generate_summary, get_recommendations_for_user
from ..utils.jwt_utils import jwt_required


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(reviews_bp, url_prefix="/books")
    # app.register_blueprint(summaries_bp, url_prefix="/summaries")
    # app.register_blueprint(recs_bp, url_prefix="/recommendations")

    @app.route("/")
    def api_root():
        return {"msg": "Welcome to Bookman API. See /apidocs for Swagger."}, 200

    @app.route("/generate-summary",methods=["POST"])
    @jwt_required()
    async def generate():
        data = request.get_json()
        return await generate_summary(data)

    @app.route("/recommendations", methods=["GET"])
    @jwt_required()
    async def recommendations():
        args = request.args
        return await get_recommendations_for_user(args)

