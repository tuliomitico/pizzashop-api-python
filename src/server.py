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
from .http.routes.register_restaurant import restaurant_blp
from .http.routes.get_profile import profile_blp
from .http.routes.update_profile import update_profile_blp
from .http.routes.get_managed_restaurant import restaurant_blp as managed_restaurant_blp
from .http.routes.sign_out import signout_blp


app = Flask(__name__)

def setup_app(app: Flask) -> None:
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    @app.errorhandler(UnauthorizedError)
    def unauthorized_error(e):
        return {"code":404,"message": str(e)},404
    api = Api()
    cors.init_app(app, resources=r'/*',supports_credentials=True)
    jwt.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    api.register_blueprint(blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(authlink)
    api.register_blueprint(restaurant_blp)
    api.register_blueprint(managed_restaurant_blp)
    api.register_blueprint(profile_blp)
    api.register_blueprint(update_profile_blp)
    api.register_blueprint(signout_blp)

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
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = 'auth'
    app.config['SECRET_KEY'] = "my-super-secret-key"
    app.config['JWT_COOKIE_SECURE'] = True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_CSRF_IN_COOKIES'] = False
    app.config['API_SPEC_OPTIONS'] = {
        "components": {
            "securitySchemes": {
                "Bearer Auth": {
                    "type": "apiKey",
                    "in": "cookies",
                    "name": "Authorization",
                    "bearerFormat": "JWT",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
                }
            }
        },
    }
    setup_app(app)
    return app
