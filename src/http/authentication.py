from flask_jwt_extended import JWTManager

from ..db.schema import User

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.filter_by(id=identity).one_or_none()

@jwt.invalid_token_loader
def my_invalid_token_loader(jwt_data):
  return {'error':'the token is invalid'}, 403

@jwt.expired_token_loader
def my_expired_token_loader(_jwt_header, jwt_data):
  return {'message': 'the token is expired'}, 403

@jwt.unauthorized_loader
def my_unauthorized_loader(jwt_data):
  return {'message': 'A valid token is missing'}, 403