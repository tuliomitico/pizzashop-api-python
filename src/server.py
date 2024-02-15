from flask import Flask
from flask_smorest import Api

from src.db.connection import db_session
from src.http.routes.get_orders import blp

app = Flask(__name__)

def setup_app(app: Flask) -> None:
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    api = Api()
    api.init_app(app)
    api.register_blueprint(blp)

def create_app(config = None) -> Flask:
    app = Flask(__name__)
    if isinstance(config,dict):
        app.config.update(config)
    app.config.from_object(config)
    app.config["API_TITLE"] = "PizzaShop API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config['OPENAPI_SWAGGER_UI_PATH'] ='/swagger-ui'
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    setup_app(app)
    return app
