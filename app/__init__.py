import os

from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///dms_db.db"
    )
    app.config["SWAGGER"] = {
        "title": "DMS API",
        "uiversion": 3,
        "openapi": "3.0.0",
        "specs_route": "/api/docs/",
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "description": "Diet Management System API",
    }

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    swagger = Swagger(app, template_file="docs/swagger_config.yml")

    with app.app_context():
        from app.models import food, foodIngredient, ingredient, nutritionInfo, person
        from app.routes import register_routes

        register_routes(api)

    return app
