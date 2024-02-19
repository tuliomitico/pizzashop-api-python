from flask import Flask
from flask_smorest import Api


from .cors import cors
from .schemas import ma
from .http.authentication import jwt
from .db.connection import db_session
from .http.routes.errors.unauthorized_error import UnauthorizedError
from .http.routes.get_orders import blp
from .http.routes.send_authentication_link import auth_blp
from .http.routes.authenticate_from_link import auth_blp as authlink


app = Flask(__name__)

def setup_app(app: Flask) -> None:
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    @app.errorhandler(UnauthorizedError)
    def unauthorized_error(e):
        return {"code":404,"message": str(e)},404
    api = Api()
    jwt.init_app(app)
    cors.init_app(app, resources=r'/*')
    ma.init_app(app)
    api.init_app(app)
    api.register_blueprint(blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(authlink)

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
