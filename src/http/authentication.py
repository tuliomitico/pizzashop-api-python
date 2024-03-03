from flask_jwt_extended import JWTManager, jwt_required
from copy import deepcopy
from functools import wraps

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
  print(_jwt_header)
  print(jwt_data)
  return {'message': 'the token is expired'}, 403

@jwt.unauthorized_loader
def my_unauthorized_loader(jwt_data):
  return {'message': 'A valid token is missing'}, 403




def jwt_required_with_doc(*args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            return jwt_required(*args, **kwargs)(func)(*f_args, **f_kwargs)

        wrapper._apidoc = deepcopy(getattr(func, "_apidoc", {}))
        wrapper._apidoc.setdefault('manual_doc', {})
        wrapper._apidoc['manual_doc']['security'] = [{"Bearer Auth": []}]
        return wrapper
    return decorator