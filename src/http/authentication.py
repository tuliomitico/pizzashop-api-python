from flask_jwt_extended import JWTManager, verify_jwt_in_request
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
  print(jwt_data)
  return {'message': 'A valid token is missing'}, 403

def jwt_required_with_doc(*args,**kwargs):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*f_args, **f_kwargs):
            verify_jwt_in_request(*args,**kwargs)
            return fn(*f_args, **f_kwargs)

        decorator._apidoc = deepcopy(getattr(fn, "_apidoc", {}))
        decorator._apidoc.setdefault('manual_doc', {})
        decorator._apidoc['manual_doc']['security'] = [{"Bearer Auth": []}]
        return decorator
    return wrapper